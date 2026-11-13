"""
Omnesight Interactive Shell & CLI
Provides terminal access to Hackmalim v1.0, Sandalfon v1.0, and cluster status.
"""

from __future__ import annotations

import argparse
import cmd
import json
import os
import shlex
from pathlib import Path
from typing import Any

import httpx

from . import __version__
from .client import DEFAULT_BASE_URL, Omnesight
from .exceptions import OmnesightError

CONFIG_ENV_VAR = "OMNESIGHT_CONFIG_FILE"
DEFAULT_CONFIG_PATH = Path.home() / ".omnesight" / "config.json"


def get_config_path() -> Path:
    """Return active CLI configuration file path."""
    override = os.environ.get(CONFIG_ENV_VAR)
    return Path(override).expanduser() if override else DEFAULT_CONFIG_PATH


def load_cli_config() -> dict[str, str]:
    """Load persisted CLI API key and base URL from disk if available."""
    path = get_config_path()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(data, dict):
        return {}
    return {
        str(k): str(v)
        for k, v in data.items()
        if isinstance(v, str) and v.strip()
    }


def save_cli_config(
    api_key: str | None = None,
    base_url: str | None = None,
) -> Path:
    """Persist CLI credentials and endpoint with owner-only (0600) permissions."""
    path = get_config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    current = load_cli_config()
    if api_key is not None:
        current["api_key"] = api_key.strip()
    if base_url is not None:
        current["base_url"] = base_url.strip().rstrip("/")
    path.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)
    return path


def resolve_credentials(
    api_key: str | None = None,
    base_url: str | None = None,
) -> tuple[str | None, str]:
    """Resolve API key and gateway URL from flags, env vars, then config file."""
    cfg = load_cli_config()
    resolved_key = (
        api_key or os.environ.get("OMNESIGHT_API_KEY") or cfg.get("api_key")
    )
    resolved_url = (
        base_url
        or os.environ.get("OMNESIGHT_BASE_URL")
        or cfg.get("base_url")
        or DEFAULT_BASE_URL
    ).rstrip("/")
    return resolved_key, resolved_url


def _mask_key(key: str | None) -> str:
    if not key:
        return "<not configured>"
    if len(key) <= 12:
        return "*" * len(key)
    return f"{key[:9]}...{key[-4:]}"


def _build_client(
    api_key: str | None = None,
    base_url: str | None = None,
    transport: httpx.BaseTransport | None = None,
) -> Omnesight:
    resolved_key, resolved_url = resolve_credentials(api_key, base_url)
    return Omnesight(
        api_key=resolved_key,
        base_url=resolved_url,
        transport=transport,
    )


def _cmd_config(args: argparse.Namespace) -> int:
    if args.api_key is None and args.base_url is None:
        resolved_key, resolved_url = resolve_credentials()
        print(f"Config path : {get_config_path()}")
        print(f"Gateway URL : {resolved_url}")
        print(f"API Key     : {_mask_key(resolved_key)}")
        return 0

    saved_path = save_cli_config(api_key=args.api_key, base_url=args.base_url)
    resolved_key, resolved_url = resolve_credentials()
    print(f"Saved config to {saved_path}")
    print(f"Gateway URL : {resolved_url}")
    print(f"API Key     : {_mask_key(resolved_key)}")
    return 0


def _cmd_status(
    args: argparse.Namespace,
    transport: httpx.BaseTransport | None = None,
) -> int:
    resolved_key, resolved_url = resolve_credentials(args.api_key, args.base_url)
    print(f"Gateway URL : {resolved_url}")
    print(f"API Key     : {_mask_key(resolved_key)}")

    client_kwargs: dict[str, Any] = {"base_url": resolved_url, "timeout": 10.0}
    if transport is not None:
        client_kwargs["transport"] = transport

    with httpx.Client(**client_kwargs) as http_client:
        for engine, path in (
            ("Hackmalim", "/api/v1/hackmalim/info"),
            ("Sandalfon", "/api/v1/sandalfon/info"),
        ):
            try:
                resp = http_client.get(path)
                if resp.status_code == 200:
                    data = resp.json()
                    ver = data.get("version", "unknown")
                    print(f"{engine:<11} : ONLINE (v{ver})")
                else:
                    print(f"{engine:<11} : HTTP {resp.status_code}")
            except httpx.HTTPError as exc:
                print(f"{engine:<11} : OFFLINE ({exc})")
                return 1
    return 0


def _cmd_hackmalim_infer(
    args: argparse.Namespace,
    transport: httpx.BaseTransport | None = None,
) -> int:
    with _build_client(args.api_key, args.base_url, transport=transport) as client:
        res = client.hackmalim.infer(
            shock_amplitude=args.shock_amplitude,
            jitter_severity=args.jitter_severity,
            leak_node=args.leak_node,
            leak_magnitude=args.leak_magnitude,
            p_max_kw=args.p_max_kw,
            t_max_c=args.t_max_c,
        )
    if args.json:
        print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        return 0
    pignn = res.stage_2_pignn or res.pignn or {}
    guard = res.enterprise_guardrail or res.guardrails or {}
    print(f"Model      : {res.model} v{res.version}")
    print(f"Target     : {res.target_entity_id}")
    print(f"Leak Node  : {pignn.get('pinpointed_node')}")
    print(f"Guardrails : approved={guard.get('is_approved')}")
    return 0


def _cmd_sandalfon_discover(
    args: argparse.Namespace,
    transport: httpx.BaseTransport | None = None,
) -> int:
    with _build_client(args.api_key, args.base_url, transport=transport) as client:
        res = client.sandalfon.discover(
            preset=args.preset,
            noise_level=args.noise_level,
            sparsity_threshold=args.sparsity_threshold,
            precursor_amp=args.precursor_amp,
            hypothesis_text=args.hypothesis,
        )
    if args.json:
        print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        return 0
    print(f"Model      : {res.model} v{res.version}")
    print(f"Eq (dx/dt) : {res.sindy.get('discovered_eq_x')}")
    print(f"ExactMatch : {res.sindy.get('exact_support_match')}")
    print(f"FFT SNR dB : {res.spectrum.get('precursor_snr_db')}")
    print(f"Popper Z   : {res.hypothesis_test.get('z_score')}")
    return 0


def _cmd_sandalfon_chat(
    args: argparse.Namespace,
    transport: httpx.BaseTransport | None = None,
) -> int:
    with _build_client(args.api_key, args.base_url, transport=transport) as client:
        res = client.sandalfon.chat(
            message=args.message,
            preset=args.preset,
        )
    if args.json:
        print(json.dumps(res.model_dump(), indent=2, ensure_ascii=False))
        return 0
    print(f"Sandalfon  : {res.spoken_reply}")
    if res.sindy:
        print(f"Equation X : {res.sindy.get('discovered_eq_x')}")
    return 0


class OmnesightShell(cmd.Cmd):
    """Interactive shell REPL for Omnesight Hackmalim and Sandalfon."""

    intro = (
        f"Omnesight Sovereign MLOps Shell v{__version__}\n"
        "Commands: status | config | sandalfon discover/chat | "
        "hackmalim infer | help | exit"
    )
    prompt = "omnesight> "

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        transport: httpx.BaseTransport | None = None,
        stdin=None,
        stdout=None,
    ) -> None:
        super().__init__(stdin=stdin, stdout=stdout)
        self.api_key = api_key
        self.base_url = base_url
        self.transport = transport
        if stdin is not None:
            self.use_rawinput = False

    def emptyline(self) -> bool:
        return False

    def _run_parsed(self, tokens: list[str]) -> None:
        parser = build_parser()
        try:
            args = parser.parse_args(tokens)
            dispatch(
                args,
                default_api_key=self.api_key,
                default_base_url=self.base_url,
                transport=self.transport,
            )
        except SystemExit:
            return
        except (OmnesightError, ValueError) as exc:
            print(f"[ERROR] {exc}", file=self.stdout)

    def do_status(self, _arg: str) -> None:
        """Show gateway endpoint, masked API key, and engine readiness."""
        self._run_parsed(["status"])

    def do_config(self, arg: str) -> None:
        """Inspect or update CLI config: config [--api-key KEY] [--base-url URL]."""
        try:
            tokens = shlex.split(arg)
        except ValueError as exc:
            print(f"[ERROR] {exc}", file=self.stdout)
            return
        self._run_parsed(["config", *tokens])

    def do_sandalfon(self, arg: str) -> None:
        """Interact with Sandalfon: sandalfon discover [preset] | chat <query>."""
        try:
            tokens = shlex.split(arg)
        except ValueError as exc:
            print(f"[ERROR] {exc}", file=self.stdout)
            return
        if not tokens:
            print("Usage: sandalfon discover [preset] | sandalfon chat <query>")
            return
        sub = tokens[0]
        rest = tokens[1:]
        if sub == "discover":
            preset = rest[0] if rest and not rest[0].startswith("-") else None
            cmd_args = ["sandalfon", "discover"]
            if preset:
                cmd_args.extend(["--preset", preset, *rest[1:]])
            else:
                cmd_args.extend(rest)
            self._run_parsed(cmd_args)
            return
        if sub == "chat":
            if not rest:
                print("Usage: sandalfon chat <query>")
                return
            query = " ".join(rest)
            self._run_parsed(["sandalfon", "chat", query])
            return
        print(f"Unknown sandalfon subcommand: {sub}")

    def do_hackmalim(self, arg: str) -> None:
        """Interact with Hackmalim: hackmalim infer [shock] [leak_node] [leak_mag]."""
        try:
            tokens = shlex.split(arg)
        except ValueError as exc:
            print(f"[ERROR] {exc}", file=self.stdout)
            return
        if not tokens or tokens[0] != "infer":
            print("Usage: hackmalim infer [shock] [leak_node] [leak_mag]")
            return
        rest = tokens[1:]
        cmd_args = ["hackmalim", "infer"]
        if rest and not rest[0].startswith("-"):
            cmd_args.extend(["--shock-amplitude", rest[0]])
            if len(rest) >= 2:
                cmd_args.extend(["--leak-node", rest[1]])
            if len(rest) >= 3:
                cmd_args.extend(["--leak-magnitude", rest[2]])
        else:
            cmd_args.extend(rest)
        self._run_parsed(cmd_args)

    def do_exit(self, _arg: str) -> bool:
        """Exit interactive shell."""
        return True

    def do_quit(self, _arg: str) -> bool:
        """Exit interactive shell."""
        return True

    def do_EOF(self, _arg: str) -> bool:
        """Exit interactive shell on EOF."""
        print()
        return True


def build_parser() -> argparse.ArgumentParser:
    """Create the top-level omnesight CLI argument parser."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--api-key", default=None, help="Override API key")
    common.add_argument("--base-url", default=None, help="Override MLOps gateway URL")

    parser = argparse.ArgumentParser(
        prog="omnesight",
        description="Omnesight Sovereign MLOps CLI & Interactive Shell",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"omnesight {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser(
        "shell",
        parents=[common],
        help="Start interactive omnesight> REPL shell",
    )
    subparsers.add_parser(
        "status",
        parents=[common],
        help="Inspect active gateway URL and engine health",
    )

    cfg_parser = subparsers.add_parser(
        "config",
        help="Read or persist CLI credentials in ~/.omnesight/config.json",
    )
    cfg_parser.add_argument("--api-key", default=None, help="Save API key")
    cfg_parser.add_argument("--base-url", default=None, help="Save MLOps gateway URL")

    hack_parser = subparsers.add_parser("hackmalim", help="Hackmalim v1.0 commands")
    hack_sub = hack_parser.add_subparsers(dest="hack_cmd", required=True)
    hack_infer = hack_sub.add_parser(
        "infer",
        parents=[common],
        help="Run closed-loop 3-layer inference",
    )
    hack_infer.add_argument("--shock-amplitude", type=float, default=1.45)
    hack_infer.add_argument("--jitter-severity", type=float, default=1.0)
    hack_infer.add_argument("--leak-node", type=int, default=2)
    hack_infer.add_argument("--leak-magnitude", type=float, default=22.5)
    hack_infer.add_argument("--p-max-kw", type=float, default=55.0)
    hack_infer.add_argument("--t-max-c", type=float, default=72.0)
    hack_infer.add_argument("--json", action="store_true", help="Print raw JSON")

    sand_parser = subparsers.add_parser("sandalfon", help="Sandalfon v1.0 commands")
    sand_sub = sand_parser.add_subparsers(dest="sand_cmd", required=True)
    sand_disc = sand_sub.add_parser(
        "discover",
        parents=[common],
        help="Run SINDy + FFT + Popperian discovery",
    )
    sand_disc.add_argument(
        "--preset",
        choices=["coupled_oscillator", "predator_prey_grid", "thermal_runaway"],
        default="thermal_runaway",
    )
    sand_disc.add_argument("--noise-level", type=float, default=0.02)
    sand_disc.add_argument("--sparsity-threshold", type=float, default=0.10)
    sand_disc.add_argument("--precursor-amp", type=float, default=0.18)
    sand_disc.add_argument("--hypothesis", default=None)
    sand_disc.add_argument("--json", action="store_true", help="Print raw JSON")

    sand_chat = sand_sub.add_parser(
        "chat",
        parents=[common],
        help="Ask Sandalfon a research question",
    )
    sand_chat.add_argument("message", help="Research question or hypothesis")
    sand_chat.add_argument(
        "--preset",
        choices=["coupled_oscillator", "predator_prey_grid", "thermal_runaway"],
        default="thermal_runaway",
    )
    sand_chat.add_argument("--json", action="store_true", help="Print raw JSON")

    return parser


def dispatch(
    args: argparse.Namespace,
    default_api_key: str | None = None,
    default_base_url: str | None = None,
    transport: httpx.BaseTransport | None = None,
) -> int:
    """Dispatch parsed CLI namespace to the matching command handler."""
    if not getattr(args, "api_key", None) and default_api_key is not None:
        args.api_key = default_api_key
    if not getattr(args, "base_url", None) and default_base_url is not None:
        args.base_url = default_base_url

    if args.command is None or args.command == "shell":
        shell = OmnesightShell(
            api_key=getattr(args, "api_key", None),
            base_url=getattr(args, "base_url", None),
            transport=transport,
        )
        shell.cmdloop()
        return 0
    if args.command == "config":
        return _cmd_config(args)
    if args.command == "status":
        return _cmd_status(args, transport=transport)
    if args.command == "hackmalim" and args.hack_cmd == "infer":
        return _cmd_hackmalim_infer(args, transport=transport)
    if args.command == "sandalfon":
        if args.sand_cmd == "discover":
            return _cmd_sandalfon_discover(args, transport=transport)
        if args.sand_cmd == "chat":
            return _cmd_sandalfon_chat(args, transport=transport)
    raise ValueError(f"Unsupported command: {args.command}")


def main(
    argv: list[str] | None = None,
    transport: httpx.BaseTransport | None = None,
) -> int:
    """CLI entrypoint registered as `omnesight` script."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return dispatch(args, transport=transport)
    except OmnesightError as exc:
        print(f"[ERROR] {exc}")
        return 1
