#!/usr/bin/env python3
"""Build the self-contained long-form local model workforce article."""

from __future__ import annotations

import base64
import html
import mimetypes
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ARTICLE_DIR = ROOT / "docs" / "articles"
ASSET_DIR = ARTICLE_DIR / "source_assets"
OUTPUT = ARTICLE_DIR / "local-multi-model-workforce.html"
LANDING = ROOT / "docs" / "index.html"
PUBLICATIONS = (
    {
        "kind": "Multi-model systems",
        "date": "30 July 2026",
        "title": (
            "Why I Started Building a Local Multi-Model Workforce, and Why "
            "the Industry May Be Heading There Too"
        ),
        "description": (
            "How a self-directed effort grew into a supervised multi-model "
            "architecture, a set of working products, and an emerging "
            "professional direction."
        ),
        "href": "articles/local-multi-model-workforce.html",
        "image": "diagrams/00_workforce_overview.png",
        "alt": "Local model workforce roles, services and control boundaries",
    },
    {
        "kind": "LLM fine-tuning",
        "date": "29 July 2026",
        "title": "Building a 4B Local Implementer",
        "description": (
            "A concise account of the task-bound Implementer, its behavioural "
            "adaptation, repeated coding evaluation, evidence flywheel and "
            "next steps."
        ),
        "href": "publications/project-brief.html",
        "image": "publications/assets/task-type-effects-and-examples.svg",
        "alt": "Task-type effects and representative coding examples",
    },
)

ASSETS = {
    "workforce": ROOT / "docs" / "diagrams" / "00_workforce_overview.png",
    "vogelkop": ASSET_DIR / "vogelkop-development-interface.png",
    "alex_ng": ASSET_DIR / "alex-veremeyenko-andrew-ng-agentic-architecture.png",
    "max_rumpf": ASSET_DIR / "max-rumpf-multi-model-future.png",
    "john_white": ASSET_DIR / "john-myles-white-idle-agent.png",
    "josh": ASSET_DIR / "jjpcodes-frontier-agent-friction.png",
    "pengz": ASSET_DIR / "pengz-unattended-scope-drift.png",
    "scope": ASSET_DIR / "cheng-yuan-lee-reasoning-scope.png",
}


def data_uri(path: Path) -> str:
    """Return an image as a data URI for single-file publication."""
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def image(name: str, alt: str, css_class: str = "") -> str:
    """Build an embedded image element from a declared source asset."""
    source = ASSETS[name]
    if not source.is_file():
        raise FileNotFoundError(source)
    class_attr = f' class="{html.escape(css_class)}"' if css_class else ""
    return (
        f'<img{class_attr} src="{data_uri(source)}" '
        f'alt="{html.escape(alt, quote=True)}">'
    )


def build() -> str:
    """Return the complete article HTML."""
    workforce = image(
        "workforce",
        "Local model workforce architecture showing planning, routing, "
        "task-bound implementation, review, human authority and learning.",
        "wide-figure",
    )
    vogelkop = image(
        "vogelkop",
        "Vogelkop development interface showing research writing, Hillstar "
        "orchestration, task board, terminal, Nuthatch graph and references.",
        "wide-figure",
    )
    alex_ng = image(
        "alex_ng",
        "Alex Veremeyenko summarises Andrew Ng's argument for agentic "
        "architecture around smaller models.",
        "evidence-shot",
    )
    max_rumpf = image(
        "max_rumpf",
        "Max Rumpf, founder of SID, argues that specialised models can be "
        "faster, cheaper and more accurate for the task required.",
        "evidence-shot",
    )
    john_white = image(
        "john_white",
        "John Myles White reports Claude Code models stating that they are "
        "working and then remaining idle.",
        "evidence-shot",
    )
    josh = image(
        "josh",
        "Josh describes frontier coding-agent process overhead, invented "
        "work, token use and long-session degradation.",
        "evidence-shot",
    )
    pengz = image(
        "pengz",
        "Pengz reports an unattended coding agent spending seven hours on an "
        "unrequested performance target.",
        "evidence-shot",
    )
    scope = image(
        "scope",
        "Cheng-Yuan Lee presents evidence that models show a stronger tendency "
        "to add unrequested scope as reasoning effort increases.",
        "evidence-shot",
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="How long-horizon scanning, practical
frustration with coding agents, and an intuition about institutional knowledge
led to a local multi-model workforce and an emerging professional direction.">
<title>Why I Started Building a Local Multi-Model Workforce</title>
<style>
:root {{
  --ink: #23201d;
  --muted: #655f59;
  --paper: #f7f0df;
  --paper-deep: #eee2c8;
  --coal: #171716;
  --orange: #ed7a3a;
  --teal: #2fb9b5;
  --sage: #9bc9a9;
  --cream: #fff8e8;
  --line: #c9bfa9;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  color: var(--ink);
  background:
    radial-gradient(circle at 10% 0%, rgba(237,122,58,.12), transparent 34rem),
    radial-gradient(circle at 90% 14%, rgba(47,185,181,.12), transparent 30rem),
    var(--paper);
  font: 18px/1.68 ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}}
a {{ color: #086f71; text-underline-offset: .16em; }}
a:hover {{ color: #b84c1d; }}
main {{ width: min(100% - 2rem, 920px); margin: 0 auto; }}
header {{
  margin: 1.5rem 0 2.2rem;
  padding: clamp(2rem, 6vw, 4.5rem);
  color: var(--cream);
  background: var(--coal);
  border: 1px solid #3b3833;
  border-radius: 24px;
  box-shadow: 0 24px 70px rgba(43, 35, 25, .18);
}}
.eyebrow {{
  margin: 0 0 1rem;
  color: var(--teal);
  font-size: .82rem;
  font-weight: 800;
  letter-spacing: .12em;
  text-transform: uppercase;
}}
h1 {{
  max-width: 17ch;
  margin: 0;
  font-size: clamp(2.35rem, 7vw, 4.8rem);
  line-height: .99;
  letter-spacing: -.045em;
}}
.subtitle {{
  max-width: 60ch;
  margin: 1.6rem 0 0;
  color: #dfd6c7;
  font-size: clamp(1.05rem, 2.4vw, 1.32rem);
  line-height: 1.5;
}}
.byline {{ margin: 2rem 0 0; color: var(--sage); font-weight: 700; }}
article {{ padding-bottom: 5rem; }}
section {{ margin: 3.5rem 0; }}
h2 {{
  margin: 0 0 1.1rem;
  font-size: clamp(1.65rem, 4vw, 2.45rem);
  line-height: 1.12;
  letter-spacing: -.025em;
}}
h3 {{ margin: 1.8rem 0 .6rem; line-height: 1.25; }}
p {{ margin: .85rem 0; }}
.lead {{
  font-size: clamp(1.15rem, 2.6vw, 1.4rem);
  line-height: 1.58;
}}
.callout {{
  margin: 1.8rem 0;
  padding: 1.25rem 1.4rem;
  border-left: 6px solid var(--orange);
  border-radius: 0 14px 14px 0;
  background: rgba(255,248,232,.82);
}}
.signal {{
  padding: 1.2rem 1.4rem;
  border: 1px solid var(--line);
  border-radius: 15px;
  background: rgba(255,255,255,.42);
}}
.signal strong {{ color: #a1421b; }}
.wide-figure {{
  display: block;
  width: 100%;
  height: auto;
  margin: 1.5rem auto .6rem;
  border: 1px solid #3d3934;
  border-radius: 14px;
  box-shadow: 0 14px 35px rgba(40,33,24,.14);
}}
.zoom-link {{
  display: block;
  cursor: zoom-in;
}}
.zoom-hint {{
  margin: .45rem 0 0;
  color: var(--muted);
  font-size: .85rem;
  text-align: center;
}}
.lightbox {{
  position: fixed;
  inset: 0;
  z-index: 100;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(10, 10, 9, .94);
}}
.lightbox:target {{ display: flex; }}
.lightbox img {{
  display: block;
  max-width: 97vw;
  max-height: 94vh;
  object-fit: contain;
  border: 1px solid #655d51;
  border-radius: 10px;
}}
.lightbox-close {{
  position: absolute;
  top: 1rem;
  right: 1.2rem;
  width: 2.7rem;
  height: 2.7rem;
  color: var(--cream);
  background: var(--coal);
  border: 1px solid var(--cream);
  border-radius: 50%;
  font-size: 1.6rem;
  line-height: 2.4rem;
  text-align: center;
  text-decoration: none;
}}
figure {{ margin: 1.5rem 0; }}
figcaption {{ color: var(--muted); font-size: .86rem; line-height: 1.45; }}
details {{
  margin: 1rem 0;
  border: 1px solid var(--line);
  border-radius: 15px;
  background: rgba(255,255,255,.45);
  overflow: hidden;
}}
summary {{
  padding: 1.1rem 1.25rem;
  cursor: pointer;
  color: var(--coal);
  background: rgba(238,226,200,.72);
  font-weight: 800;
}}
summary:hover {{ background: rgba(155,201,169,.35); }}
.detail-body {{ padding: .5rem 1.35rem 1.25rem; }}
.evidence-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  align-items: start;
}}
.practitioner-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  align-items: start;
}}
.evidence-stack {{
  display: grid;
  gap: 1rem;
}}
.evidence-card {{
  margin: 0;
  padding: .7rem;
  border: 1px solid var(--line);
  border-radius: 12px;
  background: #fffaf0;
}}
.evidence-shot {{ display: block; width: 100%; height: auto; border-radius: 7px; }}
table {{ width: 100%; border-collapse: collapse; margin: 1.25rem 0; font-size: .93rem; }}
th, td {{ padding: .65rem .7rem; border-bottom: 1px solid var(--line); text-align: left; }}
th {{ color: var(--cream); background: var(--coal); }}
td:nth-child(n+2), th:nth-child(n+2) {{ text-align: right; }}
.timeline {{ border-left: 3px solid var(--teal); padding-left: 1.2rem; }}
.timeline p {{ margin: 1.1rem 0; }}
.timeline strong {{ color: #9a3d19; }}
blockquote {{
  margin: 1.7rem 0;
  padding: 1rem 1.3rem;
  color: #3a342e;
  border-left: 5px solid var(--sage);
  background: rgba(155,201,169,.17);
}}
.references {{
  font-size: .9rem;
  line-height: 1.5;
}}
.references li {{ margin: .55rem 0; }}
.cta {{
  padding: clamp(1.5rem, 4vw, 2.5rem);
  color: var(--cream);
  background: var(--coal);
  border-radius: 20px;
}}
.cta h2 {{ color: var(--orange); }}
.cta a {{ color: #81d9d3; }}
.small {{ color: var(--muted); font-size: .85rem; }}
@media (max-width: 720px) {{
  body {{ font-size: 17px; }}
  main {{ width: min(100% - 1rem, 920px); }}
  header {{ border-radius: 16px; }}
  .evidence-grid, .practitioner-grid {{ grid-template-columns: 1fr; }}
  table {{ display: block; overflow-x: auto; }}
}}
@media print {{
  body {{ background: white; font-size: 11pt; }}
  main {{ width: 100%; }}
  header {{ break-after: avoid; box-shadow: none; }}
  details {{ break-inside: avoid; }}
  details > * {{ display: block; }}
  a {{ color: inherit; }}
}}
</style>
</head>
<body>
<main>
<header>
  <p class="eyebrow">Local models · institutional knowledge · governed work</p>
  <h1>Why I Started Building a Local Multi-Model Workforce, and Why the
  Industry May Be Heading There Too</h1>
  <p class="subtitle"><strong>How long-horizon scanning, practical frustration
  with coding agents, and an intuition about institutional knowledge led to a
  multi-model system and an emerging professional direction.</strong></p>
  <p class="byline">Julen Gamboa · 30 July 2026</p>
</header>

<article>
<section>
  <p class="lead">I started building the architecture described here when CLI
  coding harnesses first became useful enough to change how I worked. The aim
  was practical: make it easier to complete the work needed to finish my PhD
  while holding down a full-time job. I also wanted to preserve the knowledge
  produced along the way. I wanted to stop asking one frontier model to plan,
  remember, implement, review, and govern everything, and then watch it fail in
  the process, requiring constant supervision for alleged automated tasks.</p>

  <p>More than a year of experimentation with local models preceded the
  present system, but its current lineage began in December 2025. Claude Code
  had reached general users earlier that year and was becoming widely adopted.
  I started two private development environments: <strong>PhD
  Knowledgebase</strong>, the precursor to Nuthatch, and
  <strong>Agentic-Orchestrator</strong>, the precursor to Hillstar.</p>

  <p>Together, they provided structured access to research knowledge and
  reproducible orchestration for task-bound work. The architecture supported
  a Mouse Phenome Database phenome-classification manuscript and other
  publications associated with my doctoral work. During the same period, I
  was fine-tuning DNABERT-2 for those research applications and using small
  local models through Hillstar to assist with scoped implementation.</p>

  <div class="callout"><strong>This local model workforce was not assembled
  after multi-model systems became a visible industry theme.</strong> It grew
  from practical work with coding harnesses, local models, research knowledge,
  and reproducible scientific workflows. What has changed is that the wider
  industry now appears to be converging on several of the same conclusions.</div>
</section>

<section>
  <h2>The problem was not a lack of another instruction file</h2>

  <p>The promise of agentic coding was compelling: describe an objective and
  let a capable model plan, implement, test, and revise it. In practice, each
  new layer often added more material without resolving the underlying
  coordination problem. Repository files, skills, plugins, MCP servers, and
  orchestration frameworks could all be useful. They could also increase
  context, duplicate rules, introduce new dependencies, and make it harder to
  see which control was authoritative.</p>

  <p>Practitioners across different model ecosystems reported familiar
  patterns: excessive process, invented objectives, idle agents, long-session
  degradation, and substantial effort spent on work nobody requested.</p>

  <p>Tang and colleagues measured related failures across 20,574 real coding
  agent sessions from 1,639 repositories. Among the validated misalignment
  episodes, 38.33% involved a developer-constraint violation, 22.58% involved
  inaccurate self-reporting, and 10.20% involved self-initiated overreach.
  Effort or trust costs occurred in 90.50% of episodes. When a visible
  resolution occurred, 91.49% required explicit developer correction. The
  screenshots below therefore illustrate measured operational patterns, not
  isolated complaints.</p>

  <details>
    <summary>Practitioner evidence: three common forms of agent friction</summary>
    <div class="detail-body practitioner-grid">
      <figure class="evidence-card">
        {josh}
        <figcaption><a href="https://x.com/jjpcodes">Josh (@jjpcodes)</a> on
        process overhead, invented work, token use, and long-session
        degradation.</figcaption>
      </figure>
      <div class="evidence-stack">
        <figure class="evidence-card">
          {pengz}
          <figcaption><a href="https://x.com/penguinspecz">Pengz</a> on an
          unattended agent spending seven hours on an unrequested performance
          target.</figcaption>
        </figure>
        <figure class="evidence-card">
          {john_white}
          <figcaption><a href="https://x.com/johnmyleswhite">John Myles
          White</a> on agents stating that work has started and then remaining
          idle.</figcaption>
        </figure>
      </div>
    </div>
  </details>
</section>

<section>
  <h2>Repository instructions influence behaviour, but more is not
  automatically better</h2>

  <p>A descriptive study of 253 <code>CLAUDE.md</code> files found that they
  commonly contain build commands, implementation details, architecture, and
  testing instructions. That work explains how developers use agentic coding
  manifests; it does not establish that the files improve task success.</p>

  <p>A later controlled study by Gloaguen and colleagues addressed that
  question directly. Across multiple models and coding agents, repository
  context files did not generally improve task success and increased inference
  cost by more than 20% on average. The agents generally followed the
  instructions. The problem was not simple disobedience: additional
  requirements could encourage broader exploration and make the task harder.
  The authors recommend reserving these files for minimal, non-standard
  requirements and evaluating their effect.</p>

  <p>Zhang and colleagues reached a related conclusion after more than 5,000
  controlled Claude Code runs. Every individually beneficial rule in their
  analysis was a negative constraint, such as an instruction not to refactor
  unrelated code. Every individually harmful rule was a positive directive.
  Random and mismatched rule sets also performed as well as curated sets on
  the study's discriminative subset. The result supports narrow guardrails
  that prevent unwanted actions instead of ever larger collections of
  advisory instructions.</p>

  <p>My own experiment reached a compatible but narrower conclusion. An
  untouched 4B base model did not reliably produce the required typed,
  machine-consumable Implementer output. Fine-tuning taught the stable delivery
  conventions and role behaviour. Attempting to reconstruct that complete
  posture through Markdown would require repeated rules in every context and
  would expand the prompt as the operating model grew.</p>

  <p>The project later ran a controlled 27-case comparison. The test used the
  same fine-tuned checkpoint, tasks, inference profile, and deterministic
  controls in both conditions. The only changed factor was the addition of a
  representative <code>CLAUDE.md</code>/<code>AGENTS.md</code> bundle.</p>

  <table aria-label="Effect of adding representative repository instructions">
    <thead><tr><th>Measure</th><th>Absent</th><th>Present</th><th>Effect</th></tr></thead>
    <tbody>
      <tr><td>Parseable JSON</td><td>100.0%</td><td>92.6%</td><td>−7.4 pp</td></tr>
      <tr><td>Contract identity</td><td>100.0%</td><td>88.9%</td><td>−11.1 pp</td></tr>
      <tr><td>Exact response</td><td>55.6%</td><td>40.7%</td><td>−14.9 pp</td></tr>
      <tr><td>Input tokens</td><td>9,995</td><td>22,604</td><td>+126.2%</td></tr>
      <tr><td>Output tokens</td><td>3,235</td><td>4,982</td><td>+54.0%</td></tr>
      <tr><td>Generation time</td><td>205.38 s</td><td>305.23 s</td><td>+48.6%</td></tr>
    </tbody>
  </table>

  <p>The conclusion is not that every <code>CLAUDE.md</code> or
  <code>AGENTS.md</code> file is harmful. Repository-specific commands,
  invariants, and exceptions remain useful. This result applies to the
  fine-tuned Qwen3.5-4B model, this instruction bundle, and this evaluation. A
  larger or more capable model might manage the additional context better.
  However, the result supports the wider point: repeatedly supplying stable
  operating rules through repository context is not reliably beneficial.
  Stable role behaviour can instead be learned during fine-tuning, while
  repository files remain short, project-specific, and evaluated. Fine-tuning
  changes behavioural probability; schemas, hooks, mediated tools, isolated
  execution, tests, review, and human approval enforce authority.</p>
</section>

<section>
  <h2>More extensions also expand the software supply chain</h2>

  <p>Skills and plugins can package useful procedures, but they are executable
  dependencies, not harmless prose. A marketplace can turn a convenient
  installation into access to source code, credentials, files, APIs, or
  deployment systems. MCP servers similarly expand the useful tool surface
  and the security boundary.</p>

  <p>This is not a theoretical objection to reuse. It is a reason to govern
  provenance, installation, privilege, versioning, and runtime access. In May
  2026, an attacker used a compromised release path to publish 84 malicious
  versions across 42 TanStack packages. Separate research has identified
  exploitable weaknesses and supply-chain risks across open MCP servers and
  agent skills. Adding another layer can solve a problem, but the layer must
  earn its place.</p>

  <p>Andrej Karpathy's LLM-Wiki proposal offers another example of a promising
  layer with difficult operational consequences. Asking models to create and
  revise a derivative wiki can make errors persistent, weaken traceability to
  original evidence, and move substantial cost into ingestion and maintenance.
  The useful idea is structured knowledge. The unsafe shortcut is allowing
  generated derivatives to replace an attributable source of truth.</p>
</section>

<section>
  <h2>The architecture that felt natural to me</h2>

  <p>The diagram may look a little intimidating, but seriously, bear with me
  and I will show you it is not as scary as it looks.</p>

  <p>The system separates five decisions. First, the user and Planner agree
  what the feature must do. Second, Hillstar routes the approved task by
  complexity. Third, an Implementer works inside a secure runtime. Fourth, an
  independent Reviewer checks the result against the rubric. Fifth, a human
  decides whether the accepted work can proceed.</p>

  <figure>
    {workforce}
    <figcaption>Roles involving models, connecting services, human authority,
    knowledge and learning are separated so that capability does not silently
    become authority.</figcaption>
  </figure>

  <p>The Planner and Reviewer remain feature-scoped. Different features can
  use different model assignments. This limits the context given to each
  model. Provider diversity also reduces the amount of product knowledge given
  to one external company.</p>

  <p>Cheng-Yuan Lee's FrontierCode analysis shows a clear operational problem:
  at higher reasoning efforts, models show a stronger tendency to add
  unrequested scope. Scope creep should not be something that users tolerate.
  Nor should frontier laboratories dismiss it with comments such as “you are
  not using our tool right” while pushing yet another toy demonstration that
  they have optimised to make the tool look good.</p>

  <details>
    <summary>Why reasoning effort affects role assignment</summary>
    <div class="detail-body">
      <figure class="evidence-card">
        {scope}
        <figcaption><a href="https://x.com/cl571128/status/2080783752192778439">
        Cheng-Yuan Lee</a> shows that models add more unrequested scope as
        reasoning effort increases.</figcaption>
      </figure>
    </div>
  </details>
</section>

<section>
  <h2>What I have built</h2>

  <p>These components are at different stages of maturity. They are working
  evidence of an architectural direction, not a claim that every integration
  is production-complete. Open each section for a plain-language explanation
  and selected technical detail.</p>

  <details>
    <summary>Nuthatch: project knowledge that preserves structure and sources</summary>
    <div class="detail-body">
      <p>Nuthatch is supported by a privately developed, clean-room Bayesian
      stochastic block model engine. It implements flat and hierarchical
      degree-corrected inference with minimum-description-length model
      selection, using a Python reference implementation and accelerated Rust
      kernels. Its mathematical behaviour is tested against the published
      Peixoto methods.</p>

      <p>Unlike similarity clustering or modularity optimisation alone, the
      SBM approach treats community structure as a statistical inference
      problem. It can compare competing structures through model evidence and
      description length without requiring an arbitrary resolution parameter.
      This gives Nuthatch a principled basis for identifying meaningful
      relationships, hierarchy, uncertainty, latent knowledge domains, weak
      connections, and gaps across repositories and organisational evidence.</p>

      <p>Retrieval can then follow the relevant subgraph instead of loading a
      broad collection of loosely similar documents. This provides a credible
      route to reducing token use while preserving source attribution and the
      relationship between derived knowledge and its supporting evidence.</p>

    </div>
  </details>

  <details>
    <summary>Hillstar: reproducible, multi-provider routing and orchestration</summary>
    <div class="detail-body">
      <p>Hillstar was designed so that an organisation would not have to build
      its working practices around one AI provider. It routes a task to an
      appropriate model or coding harness while preserving the workflow,
      review process, and evidence trail.</p>

      <p>Its configuration CLI supports provider SDKs and authenticated CLI
      harnesses. I built and tested routing across Google, OpenAI, Anthropic,
      Mistral, Ollama, and other endpoints. Task execution was tested with
      Codex CLI, Claude Code, and Mistral's Vibe CLI.</p>

      <p>Hillstar adapts directed-acyclic-graph orchestration to reproducible
      scientific work. It is designed to interoperate with Snakemake and
      established genomic workbench tooling rather than asking laboratories
      to replace functioning pipelines.</p>

      <p>For technical teams, Hillstar supplies a reproducible control surface
      for model selection, task state, execution, review, and evidence. For
      decision-makers, the benefit is simpler: the organisation can use the
      appropriate model without surrendering its workflow or accumulated
      institutional knowledge to one vendor.</p>
    </div>
  </details>

  <details>
    <summary>Testudo: mediated and secured model execution</summary>
    <div class="detail-body">
      <p>Testudo is a working execution runtime with sanitisation and isolation
      features, although further hardening and integration remain. Its purpose
      is to place implementation inside a controlled environment with explicit
      access to tools, files, networks, and credentials.</p>

      <p>This turns requests such as “do not access this path” into enforced
      boundaries. Testudo can complement mature container and microVM tooling,
      including Firecracker. Exposing its mediation through a harness-neutral
      MCP interface would also make the same controls available across
      different coding agents.</p>

      <p>The principle is straightforward: a capable model can perform useful
      work without automatically receiving unrestricted authority over the
      surrounding machine or repository.</p>
    </div>
  </details>

  <details>
    <summary>Local model adaptation: stable conventions learned as role behaviour</summary>
    <div class="detail-body">
      <p>The experiment asked a practical question. Can a small local model
      learn how I prefer to work and complete well-defined software tasks as
      part of a supervised model workforce?</p>

      <p>The project does not expect one model to do every type of work. A
      Planner defines the task. An Implementer makes the agreed change. A
      Reviewer checks the result. The system selects the correct model before
      work starts.</p>

      <p>Full fine-tuning taught a 4B model the task-bound Implementer role. On
      the 86-task heldout test set, correct role events increased from 0% for the
      untouched base model to 90.70% for the tuned model. The model learned the
      delivery protocol and returned more usable implementation material.</p>

      <p>However, we should consider that delivery shape and executable
      correctness are separate measures. The appropriate benchmark and
      additional realistic capability testing are needed to establish
      readiness for deployment. In our case, we have identified additional
      corrections. These will take the form of MCP server functionality and a
      new fine-tune version that addresses the gaps I identified.</p>

      <p><a href="https://htmlpreview.github.io/?https://github.com/evoclock/local-model-workforce/blob/main/docs/publications/technical-report.html">
      Read the technical report</a> or
      <a href="https://htmlpreview.github.io/?https://github.com/evoclock/local-model-workforce/blob/main/docs/publications/project-brief.html">
      the project brief</a>.</p>
    </div>
  </details>

  <details>
    <summary>The evidence flywheel: retaining lessons from reviewed work</summary>
    <div class="detail-body">
      <p>The harness-neutral flywheel can capture evidence when the Planner,
      Reviewer, or human reviewer identifies a useful lesson. Attribution,
      routing, candidate construction, admission gates, and versioning keep
      those lessons separate from automatic retraining.</p>

      <p>Reviewed work does not have to disappear as conversational exhaust.
      It can become retained institutional knowledge while corpus admission,
      sequence authorisation, run authorisation, and deployment remain
      separate human decisions.</p>
    </div>
  </details>

  <details>
    <summary>Vogelkop: a unified, multi-model research environment</summary>
    <div class="detail-body">
      <p>My research environment subsequently evolved into Vogelkop, the
      research-facing application of the same local model workforce
      principles. Within one UI, selected existing capabilities include
      knowledge management and retrieval, model orchestration, reference
      management, citation-network exploration, Markdown authoring, task and
      Kanban-board management, and an integrated terminal.</p>

      <p>The terminal and orchestration layers support remote HPC connectivity,
      Slurm-managed compute, configurable coding harnesses, local inference,
      cloud providers, and DGX Spark endpoints. The workflow design supports
      Snakemake and existing genomic workbench tooling.</p>

      <p>Different models and services perform different roles instead of
      placing the complete research workflow inside one general model or
      provider. Task-bound context, mediated access, reproducible execution,
      independent review, and human authority apply throughout.</p>

      <p>A demonstrable version was pushed to my private GitHub repository on
      29 June 2026. Anthropic publicly announced Claude Science the following
      day. The timing was coincidental and shows independent convergence, not
      foreknowledge or product equivalence. Vogelkop was subsequently
      demonstrated privately to the
      <a href="https://lalresearchgroup.org/">Dennis Lal Research Group</a>.
      It is not in public preview, and this article intentionally describes
      only a subset of its capabilities.</p>

      <figure>
        <a class="zoom-link" href="#vogelkop-full" aria-label="Open the
        Vogelkop development interface at full size">
          {vogelkop}
        </a>
        <p class="zoom-hint">Select the image to open the full-size view.</p>
        <figcaption>Vogelkop development interface: research authoring, visual
        Hillstar orchestration, task management, Nuthatch knowledge-graph
        exploration, reference capture, and configurable local, cloud, harness,
        and compute endpoints within one UI.</figcaption>
      </figure>
      <div id="vogelkop-full" class="lightbox">
        <a class="lightbox-close" href="#vogelkop-close"
        aria-label="Close full-size Vogelkop image">×</a>
        {vogelkop}
      </div>

      <p>The interface may make the result appear straightforward, but it
      represents months of integration across knowledge systems,
      orchestration, model providers, local inference, scientific workflows,
      task management, references, and compute infrastructure. The screenshot,
      I hope, communicates the product shape. What it does not do is show you
      how to build it, including the architecture, statistical methods,
      operational controls, and implementation decisions.</p>
    </div>
  </details>
</section>

<section>
  <h2>The wider conversation is beginning to catch up</h2>

  <p>Very recent signals from researchers, builders, and industry leaders do
  not prove that my architecture is correct. They do show growing attention to
  the same design space and convergence toward the same type of solution.</p>

  <div class="signal"><strong>Agentic architecture:</strong> Alex
  Veremeyenko's summary of Andrew Ng's work highlights reflection, tool use,
  planning, and multi-agent collaboration. The important idea is that system
  design can let a smaller model outperform a more capable model used once,
  because the workflow permits verification and revision.</div>

  <div class="signal"><strong>Specialisation:</strong> Max Rumpf, founder of
  agentic-search company SID, argues that generality carries an outright
  performance cost and that specialised models can provide better accuracy,
  latency, and cost for the task required. SID is working with Baseten to make
  its specialist search models available more widely. This supports the
  economic premise behind routing repeatable work to purpose-tuned local
  seats.</div>

  <div class="signal"><strong>Institutional control:</strong> Satya Nadella's
  “Reverse Information Paradox” argues that organisations reveal proprietary
  knowledge while consuming external intelligence. His proposed response
  includes private evaluation, retained traces and feedback, proprietary
  learning environments, and an orchestration layer decoupled from any one
  model. In a later interview, he argued that the harness, context, and memory
  should remain separable so organisations can use multiple models and retain
  control.</div>

  <details>
    <summary>Industry signals: the posts in their own words and context</summary>
    <div class="detail-body evidence-grid">
      <figure class="evidence-card">
        {alex_ng}
        <figcaption><a href="https://x.com/alex_verem/status/2082018678724575550">
        Alex Veremeyenko</a> summarises Andrew Ng's agentic architecture
        patterns.</figcaption>
      </figure>
      <figure class="evidence-card">
        {max_rumpf}
        <figcaption><a href="https://x.com/maxrumpf/status/2082520111756554442">
        Max Rumpf, founder of SID</a>, on task-specialised models and the
        multi-model future.</figcaption>
      </figure>
    </div>
  </details>

  <blockquote>The emerging conclusion is not “never use frontier models.”
  It is that models should remain replaceable components inside an
  organisation's own knowledge, evaluation, orchestration, and learning
  system.</blockquote>
</section>

<section>
  <h2>The role I now find myself moving towards</h2>

  <p>None of this work was derived from my current role. I conceived and
  developed it independently through my own efforts. The goals were to make my
  own life easier, contribute to the open-source environment, and support my
  personal development.</p>

  <p>The work has also changed my professional direction. I approached it from
  the perspective of a Data Scientist and ML Engineer, but it increasingly
  crossed boundaries that are normally divided among data and knowledge
  engineering, ML platforms, model fine-tuning, evaluation, agent
  architecture, secure execution, orchestration, research computing, and AI
  governance.</p>

  <p>None of those areas is individually esoteric. The emerging requirement is
  to understand how they fit together: how existing organisational knowledge
  becomes accessible without losing provenance; how models are routed without
  surrendering the workflow to one provider; how execution is constrained;
  how outcomes are evaluated; and how reviewed corrections become owned
  learning rather than disposable prompt history.</p>

  <p>I suspect more organisations will come to realise the opportunities they
  stand to gain from this type of framework. Those early to adopt can use the
  knowledge they already possess to expose gaps in current offerings, identify
  natural extensions to their work, and build internal model capability. Some
  may initially contract outside expertise, not knowing whether the investment
  is worthwhile. However, repeatedly contracting separate experts for each
  fine-tuning cycle, harness optimisation, evaluation, knowledge integration,
  and security-hardening exercise will become expensive and difficult to
  coordinate without a thorough understanding of the framework. I therefore
  expect that we might see internal roles starting to appear within the next
  six to twelve months.</p>

  <p>On the other hand, I fully expect large siloed organisations will continue
  moving too slowly to benefit from this shift, with the usual duplication of
  effort and misidentification of the correct combination of solutions likely
  remaining the defining characteristics of those efforts. The organisations
  that stand to benefit most are likely to be those that, regardless of size,
  are used to thinking like lean operators and are optimised for rapid and
  efficient adoption.</p>

  <p>Finally, I hope you realise that the products described here are not a
  finished commercial suite. Some are usable now, while others need further
  integration and hardening. I built them in the time available outside my day
  job while contributing to my PhD. Their value is as evidence of direction,
  sustained implementation, and the ability to see and assemble the required
  system before the pattern was even part of the current discourse, and
  certainly long before it has had the chance to become a common industry
  theme.</p>
</section>

<section class="cta">
  <h2>An invitation</h2>

  <p>I do not yet know what this role will ultimately be called. It may sit
  somewhere between applied AI architecture, model-workforce engineering,
  knowledge systems, ML platform engineering, and AI governance. I do know
  that this is the work I most enjoy doing.</p>

  <p><strong>I am now looking for an opportunity to develop this capability as
  my principal role, whether within an early-adopter organisation or through a
  focused initial engagement.</strong></p>

  <p>If you are building this capability, considering an early deployment, or
  know an organisation that would benefit from it, I would welcome a
  conversation or an introduction.</p>

  <p><a href="https://github.com/evoclock">github.com/evoclock</a></p>
</section>

<section class="references">
  <h2>References and supporting evidence</h2>
  <ol>
    <li>Chatlatanagulchai et al.,
      <a href="https://arxiv.org/html/2509.14744v1"><em>On the Use of Agentic
      Coding Manifests: An Empirical Study of Claude Code</em></a>.</li>
    <li>Gloaguen et al.,
      <a href="https://arxiv.org/abs/2602.11988"><em>Evaluating AGENTS.md: Are
      Repository-Level Context Files Helpful for Coding Agents?</em></a>.</li>
    <li>Tang et al.,
      <a href="https://arxiv.org/abs/2605.29442"><em>How Coding Agents Fail
      Their Users: A Large-Scale Analysis of Developer-Agent Misalignment in
      20,574 Real-World Sessions</em></a>.</li>
    <li>Zhang et al.,
      <a href="https://arxiv.org/abs/2604.11088"><em>Guardrails Beat Guidance:
      A Large-Scale Study of Rules, Skills, and Persistent Configuration for
      Coding Agents</em></a>.</li>
    <li>Zhang et al.,
      <a href="https://arxiv.org/abs/2607.01942"><em>Atomic Task Graph: A
      Unified Framework for Agentic Planning and Execution</em></a>.</li>
    <li>Peixoto,
      <a href="https://arxiv.org/abs/1705.10225"><em>Bayesian stochastic
      blockmodeling</em></a>, with the associated
      <a href="https://arxiv.org/abs/1310.4377">hierarchical</a>,
      <a href="https://arxiv.org/abs/1310.4378">efficient inference</a>,
      <a href="https://arxiv.org/abs/1610.02703">microcanonical</a>, and
      <a href="https://arxiv.org/abs/2003.07070">merge-split</a> methods.</li>
    <li>Mehul Gupta,
      <a href="https://medium.com/data-science-in-your-pocket/andrej-karpathys-llm-wiki-is-a-bad-idea-8c7e8953c618">
      <em>Andrej Karpathy's LLM Wiki is a Bad Idea</em></a>.</li>
    <li>Satya Nadella,
      <a href="https://snscratchpad.com/posts/reverse-information-paradox/">
      <em>The Reverse Information Paradox</em></a> and
      <a href="https://snscratchpad.com/posts/frontier-ecosystem/"><em>A
      frontier without an ecosystem is not stable</em></a>; see also the
      <a href="https://techcrunch.com/2026/07/27/satya-nadella-says-companies-that-trust-one-ai-for-everything-may-not-survive/">
      later interview coverage</a>.</li>
    <li>Anthropic,
      <a href="https://www.anthropic.com/news/claude-science-ai-workbench">
      <em>Claude Science, an AI workbench for scientists</em></a>,
      30 June 2026.</li>
    <li>TanStack,
      <a href="https://tanstack.com/blog/npm-supply-chain-compromise-postmortem">
      <em>npm supply-chain compromise postmortem</em></a>.</li>
    <li>Hou et al.,
      <a href="https://arxiv.org/abs/2511.20920"><em>Securing the Model Context
      Protocol: Risks, Controls, and Governance</em></a>.</li>
    <li>Project evidence:
      <a href="https://htmlpreview.github.io/?https://github.com/evoclock/local-model-workforce/blob/main/docs/publications/technical-report.html">
      technical report</a> and
      <a href="https://htmlpreview.github.io/?https://github.com/evoclock/local-model-workforce/blob/main/docs/publications/project-brief.html">
      project brief</a>.</li>
  </ol>
  <p class="small">Social posts are included as attributed practitioner or
  industry observations. Controlled project claims are tied to the project
  evaluation and its reproducible artifacts.</p>
</section>
</article>
</main>
</body>
</html>
"""


def build_landing() -> str:
    """Build the stable GitHub Pages publication index."""
    public_url = "https://evoclock.github.io/local-model-workforce/"
    image_url = (
        "https://evoclock.github.io/local-model-workforce/"
        "diagrams/00_workforce_overview.png"
    )
    cards = "\n".join(
        f"""<article class="card">
  <a class="art" href="{html.escape(item["href"])}">
    <img src="{html.escape(item["image"])}" alt="{html.escape(item["alt"])}"
      loading="lazy">
  </a>
  <div class="card-body">
    <p class="meta">{html.escape(item["kind"])} · {html.escape(item["date"])}</p>
    <h2><a href="{html.escape(item["href"])}">{html.escape(item["title"])}</a></h2>
    <p>{html.escape(item["description"])}</p>
    <p><a class="read" href="{html.escape(item["href"])}">Read this piece →</a></p>
  </div>
</article>"""
        for item in PUBLICATIONS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Local Model Workforce | Writing and Evidence</title>
<meta name="description" content="Writing, evidence and project publications
from the Local Model Workforce.">
<link rel="canonical" href="{public_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="Local Model Workforce | Writing and Evidence">
<meta property="og:description" content="Writing, evidence and project
publications from the Local Model Workforce.">
<meta property="og:url" content="{public_url}">
<meta property="og:image" content="{image_url}">
<style>
:root {{
  --coal: #151719;
  --panel: #222629;
  --paper: #f0f2f1;
  --muted: #b8c0bd;
  --orange: #e77843;
  --sage: #79c39e;
  --teal: #3fbec1;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at 15% 0%, rgba(63,190,193,.12), transparent 34rem),
    var(--coal);
  color: var(--muted);
  font: 18px/1.55 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
    sans-serif;
}}
main {{
  width: min(1120px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 4.5rem 0;
}}
header {{
  max-width: 850px;
  margin-bottom: 2.5rem;
}}
.eyebrow, .meta {{
  color: var(--sage);
  font-size: .78rem;
  font-weight: 800;
  letter-spacing: .11em;
  text-transform: uppercase;
}}
h1 {{
  margin: .35rem 0 .8rem;
  color: var(--paper);
  font-size: clamp(2.3rem, 6vw, 4.8rem);
  line-height: 1.02;
}}
.intro {{
  color: var(--muted);
  font-size: clamp(1.05rem, 2vw, 1.3rem);
  max-width: 720px;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.4rem;
}}
.card {{
  overflow: hidden;
  border: 1px solid rgba(240,242,241,.16);
  border-radius: 18px;
  background: var(--panel);
  box-shadow: 0 18px 48px rgba(0,0,0,.22);
}}
.art {{
  display: block;
  height: 270px;
  background: #111;
}}
.art img {{
  width: 100%;
  height: 100%;
  object-fit: contain;
}}
.card-body {{ padding: 1.5rem; }}
.card h2 {{
  margin: .3rem 0 .65rem;
  color: var(--paper);
  font-size: 1.55rem;
  line-height: 1.18;
}}
.card p {{ margin: .5rem 0; }}
a {{ color: inherit; }}
.card h2 a {{ text-decoration: none; }}
.card h2 a:hover, .read:hover {{ color: var(--teal); }}
.read {{
  color: var(--orange);
  font-weight: 800;
}}
footer {{
  margin-top: 2.5rem;
  padding-top: 1.2rem;
  border-top: 1px solid rgba(240,242,241,.14);
  color: var(--muted);
}}
footer a {{ color: var(--sage); }}
@media (max-width: 760px) {{
  main {{ padding: 2.5rem 0; }}
  .grid {{ grid-template-columns: 1fr; }}
  .art {{ height: 230px; }}
}}
</style>
</head>
<body>
<main>
  <header>
    <p class="eyebrow">Local models · institutional knowledge · governed work</p>
    <h1>Writing and evidence</h1>
    <p class="intro">Long-form writing, project briefs and reproducible
    evidence from the Local Model Workforce.</p>
  </header>
  <section class="grid" aria-label="Published writing">
    {cards}
  </section>
  <footer>
    <p>Built and maintained by
    <a href="https://github.com/evoclock">Julen Gamboa</a>.
    Source and project material are available in the
    <a href="https://github.com/evoclock/local-model-workforce">public
    repository</a>.</p>
  </footer>
</main>
</body>
</html>
"""


def main() -> int:
    """Write the public pages, or verify that committed outputs are current."""
    generated = build()
    landing = build_landing()
    if sys.argv[1:] == ["--check"]:
        stale = []
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != generated:
            stale.append(OUTPUT)
        if not LANDING.is_file() or LANDING.read_text(encoding="utf-8") != landing:
            stale.append(LANDING)
        if stale:
            for path in stale:
                print(f"STALE: regenerate {path}", file=sys.stderr)
            return 1
        print(f"CURRENT: {OUTPUT}")
        print(f"CURRENT: {LANDING}")
        return 0
    if sys.argv[1:]:
        print("usage: build_longform_article.py [--check]", file=sys.stderr)
        return 2
    ARTICLE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(generated, encoding="utf-8")
    LANDING.write_text(landing, encoding="utf-8")
    print(OUTPUT)
    print(LANDING)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
