"""
Omnesight Python SDK - Quickstart Example
Demonstrates sovereign MLOps calls against Hackmalim v1.0, Sandalfon v1.0,
and operational telemetry pipelines.
"""

import os
from omnesight import Omnesight


def main():
    api_key = os.environ.get("OMNESIGHT_API_KEY")
    sandbox_mode = not api_key or os.environ.get("OMNESIGHT_SANDBOX") in ("1", "true", "True")

    client = Omnesight(
        api_key=api_key,
        base_url=os.environ.get("OMNESIGHT_BASE_URL"),
        sandbox=sandbox_mode,
    )

    mode_label = "Sandbox (Deterministic Offline Simulation)" if client.is_sandbox else "Production Gateway"
    print(f"Omnesight Sovereign MLOps Client Initialized [{mode_label}]")

    # 1. Sandalfon v1.0: Discover sparse differential equations & FFT wave precursors
    print("\n[Step 1] Sandalfon v1.0 Scientific Discovery...")
    try:
        discovery = client.sandalfon.discover(
            preset="thermal_runaway",
            noise_level=0.02,
            sparsity_threshold=0.10,
            precursor_amp=0.18,
            hypothesis_text="Check cable thermal runaway harmonics before outage",
        )
        print(f"  Discovered ODE X : {discovery.sindy.get('discovered_eq_x')}")
        print(f"  Precursor SNR dB : {discovery.spectrum.get('precursor_snr_db')}")
        print(f"  Popper Z-Score   : {discovery.hypothesis_test.get('z_score')}")

        dialogue = client.sandalfon.chat(
            message="Analyse le couplage thermique avec un signal faible sur les câbles",
            preset="thermal_runaway",
        )
        print(f"  Sandalfon Reply  : {dialogue.spoken_reply}")
    except Exception as e:
        print(f"Sandalfon notice (requires live MLOps API): {e}")

    # 2. Hackmalim v1.0: Closed-loop Liquid ODE + Kirchhoff PI-GNN + Causal SAT Verifier
    print("\n[Step 2] Hackmalim v1.0 Sovereign 3-Layer Control...")
    try:
        res = client.hackmalim.infer(
            shock_amplitude=1.45,
            leak_node=2,
            leak_magnitude=22.5,
            p_max_kw=55.0,
            t_max_c=72.0,
        )
        pignn = res.stage_2_pignn or res.pignn or {}
        guardrail = res.enterprise_guardrail or res.guardrails or {}
        print(f"  Target Entity    : {res.target_entity_id}")
        print(f"  Pinpointed Node  : {pignn.get('pinpointed_node')}")
        print(f"  Guardrail Valid  : {guardrail.get('is_approved')}")
    except Exception as e:
        print(f"Hackmalim notice (requires live MLOps API): {e}")

    print("\nQuickstart completed.")


if __name__ == "__main__":
    main()
