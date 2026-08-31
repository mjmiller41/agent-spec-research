---
type: Methodology
title: Ionizable Lipid Nanoparticle Formulation Protocol
description: Microfluidic assembly and characterization protocol for lipid-encapsulated Cas9 mRNA and sgRNA.
tags: [protocol, methodology, lnp, formulation]
status: stable
generated:
  by: science-agent/gemini-2.5-pro
  at: 2026-08-31T09:00:00Z
verified:
  - by: human:formulation-chemist
    at: 2026-08-31T09:30:00Z
sources:
  - id: microfluidic-standard-sop
    resource: https://protocols.io/view/microfluidic-lnp-assembly-v4
    title: Standard Operating Procedure for Microfluidic LNP Assembly
    author: Nanomedicine Consortium
---

# Formulation Overview

Lipid nanoparticles are formulated using a four-component lipid mixture at molar ratios of 50:10:38.5:1.5 (Ionizable Lipid : DSPC : Cholesterol : PEG-Lipid).[^microfluidic-standard-sop]

# Step-by-Step Procedure

1. **Aqueous Phase Preparation**: Dissolve Cas9 mRNA and synthetic sgRNA in 50 mM sodium acetate buffer (pH 4.0).
2. **Organic Phase Preparation**: Dissolve lipid mixture in 100% anhydrous ethanol.
3. **Microfluidic Mixing**: Combine phases at a 3:1 volumetric flow rate ratio using an staggered herringbone micromixer.
4. **Dialysis & Concentration**: Buffer exchange against $1\times$ PBS (pH 7.4).

# Associated Research

* Utilized by [Zhang Lab In Vivo Trial](/studies/zhang-lab-2023.md).
* Core delivery vector synthesized in [CRISPR Delivery Compendium](/synthesis/crispr-cas9-delivery.md).

[^microfluidic-standard-sop]: Standard Operating Procedure for Microfluidic LNP Assembly
