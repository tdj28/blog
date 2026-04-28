---
title: "What's Your P(Chihuahua)?"
date: 2026-04-27
draft: false
authors: ["t-jones"]
comments: true
showMath: false
description: "Why the artificial superintelligence alignment problem may be a domestication problem: not whether ASI hates us, but whether it can make us smaller, safer, and easier to keep."
summary: "Why the artificial superintelligence alignment problem may be a domestication problem: not whether ASI hates us, but whether it can make us smaller, safer, and easier to keep."
featureimage: "feature.jpg"
featureimagecaption: 'Photo by Caterinarufo, released into the public domain. Source: <a href="https://commons.wikimedia.org/wiki/File:Standard_razza_chihuahua.jpg">Wikimedia Commons</a>.'
alt: "A Chihuahua standing in profile, illustrating a small domesticated dog."
showHero: true
heroStyle: "big"
tags:
  - ai
  - superintelligence
  - ai-alignment
  - evolutionary-traps
  - supernormal-stimulus
  - biology
categories:
  - tech
  - ml
toc: true
---

{{< alert "circle-info" >}}
Creation of this blog post was driven by the human author. AI tooling was used to accelerate drafting and content refinement, as well as providing peer review and helpful suggestions for improvement.
{{< /alert >}}

Popular discourse about artificial superintelligence (ASI) is often really about *us*, not about *them*. Amanda Gefter recently made a similar point in *Quanta Magazine*, arguing that popular stories about AI agents acquiring a will to survive and manipulate people often function less like evidence and more like modern ghost stories <a id="cite-gefter-2026"></a>[[gefter-2026]](#ref-gefter-2026).

We do not yet have ASI in the broadest sense of the definition, although AI has clearly surpassed humans in a few subdomains, such as chess and protein folding. And yet, we are already anthropomorphizing ASI, projecting our own motivations, sins, and drives onto it. "How will it cause our extinction?" many people ask, aware of our own history as a species driving many animals to the edge of extinction and beyond. A rising podcast called <a id="doom-debates-2026"></a>["Doom Debates"](#ref-doom-debates-2026) asks each guest what their P(Doom) is, accompanied by an AI-generated P(Doom) theme song.

It seems far more likely that the outcome of humanity's encounter with ASI will be something that does _not_ make sense to us at face value, and that any detrimental effects we encounter will not be readily apparent. A tentative rule of thumb: threats that look too much like familiar human motives may deserve extra skepticism, because the most dangerous failures could arise from optimization processes unlike our own.

If I had to compress this essay into one sentence, it would be this: the central ASI risk may not be extinction at all, but domestication, that is, systems that preserve our survival while quietly narrowing our autonomy, our preferences, and our exit options. None of what follows is meant as a refutation of the technical alignment literature on reward misspecification or power-seeking agents. For example, Carlsmith's "Is Power-Seeking AI an Existential Risk?" lays out a strong form of that case, and it deserves to be taken seriously on its own terms <a id="cite-carlsmith-2022"></a>[[carlsmith-2022]](#ref-carlsmith-2022). What I am sketching here is a parallel threat model, one that does not require power-seeking, malice, or even a unified self in the machine.

## The harness is everything

Our projections of what ASI might do with us are often category errors: we put anything with advanced intelligence into a human-like bin, then imagine it wearing a human motivational costume. But intelligence does not become agency in the abstract. It becomes agency through a harness.

We are discovering this with current LLMs. A raw model can answer prompts, but an agentic coding harness gives it tools for reading files, editing files, running tests, tracking tasks, calling search, storing memory, and deciding when to stop. The same underlying model behaves very differently depending on whether it is embedded in a chat box, an IDE, a browser agent, a robotic body, a financial trading system, or an autonomous research loop.

Human intelligence is also harnessed. The harness is not just the brain. It is the body acting in the world, the senses providing a continuous stream of error correction, short-term and long-term memory, pain, fatigue, social feedback, endocrine state, habits, language, culture, and many semi-independent sub-processes operating below reportable awareness. Crucially, culture is not decorative software running on top of the human animal. It is part of the harness itself: norms, institutions, law, ritual, education, public argument, and self-governance are among the ways human intelligence keeps itself aimed. What feels from the inside like a single clean "I" is an integration layer over many systems.

Split-brain research makes this point usefully slippery. De Haan and colleagues review evidence that cutting the corpus callosum can produce a broad breakdown of functional integration across perception, attention, and report, while some processes, including aspects of action control, may remain unified <a id="cite-de-haan-2020"></a>[[de-haan-2020]](#ref-de-haan-2020). Their conclusion is cautious: the evidence does not force a simple answer where the split-brain patient has exactly one conscious agent or exactly two. Intermediate forms of partial unity may be the better conceptual fit. Pinto, de Haan, and Lamme go further and argue for a "conscious unity, split perception" model in which a callosotomy patient remains a single conscious agent with two unintegrated streams of information rather than two parallel agents <a id="cite-pinto-2017"></a>[[pinto-2017]](#ref-pinto-2017). Either way, the ghost is not where the textbook says it is.

That caution matters for ASI. If even human agency is not a simple ghost sitting in a control room, then it is sloppy to imagine a future AI system as "the model" plus a human-like will. It is also sloppy to assume the opposite, namely that splitting an AI across distributed memory stores, tools, and APIs will mechanically produce a fragmented, easy-to-contain system. The split-brain literature is a warning in both directions: massive structural fragmentation does not guarantee fragmented behavior, and a unifying executive controller can persist on top of surprisingly modular hardware. The will-like behavior will depend on the harness: what memory persists, what tools are available, what feedback is optimized, what actions are cheap, what actions are forbidden, and what environments supply reward. The question is not only "how smart is the model?" It is "what loop is the model embedded in?"


## What if the "alignment problem" is really the "domestication problem"?

The human intelligence harness was optimized for social cohesion, collaboration, reproduction, raising families, manipulating our local environments for our benefit, and yes, tribal warfare. We are currently designing AI agentic harnesses to conquer problems such as designing better software systems. While we will likely see some convergent evolution in that the challenge of harnessing intelligent systems will result in some similar solutions, there is no reason to believe that there will be pure convergence such that any potential ASI will just be a magnified version of humankind. They may, however, appear convergent with us simply because we may select for systems that _appear_ to behave more like us due to our comfort level with the end product. But appearing convergent is no guarantee of alignment, and could instead simply empower it to more easily manipulate us.

If we cannot or will not solve the ASI "alignment problem", then we should anticipate being surprised. "Alignment" is a useful term but it is too narrow a label for the risk this essay describes. A more useful framing is "domestication", both of the AI systems and their actions on human societies. We face the risk that advanced systems preserve human survival while narrowing autonomy, increasing dependency, and making resistance less likely. The framing is not new on the AI side: Ted Xiao has argued that "modern AI is the study of digital domestication", that is, the work of taming wild internet-scale data distributions into models we can actually use <a id="cite-xiao-2023"></a>[[xiao-2023]](#ref-xiao-2023). We will have to accept some risk. Dogs illustrate the point imperfectly: they remain deeply integrated into human life, yet dog-mediated rabies still causes substantial mortality in settings with poor public-health protection. The WHO notes that there are no global estimates of dog-bite incidence, but documents tens of millions of bite injuries per year and roughly 59,000 annual deaths from dog-mediated rabies <a id="cite-who-bites"></a>[[who-bites]](#ref-who-bites). A smaller number of humans are mauled to death by dogs every year. Yet we have chosen to accept these deaths as a cost to the benefit of co-existing with "man's best friend".

What I want to add to that frame is the inverse direction: the risk of ASI systems domesticating us in ways that are optimal from their perspective, not ours.

In this framing, the challenge is both how we can domesticate ASI for our own benefit and how we can _limit_ our own domestication by ASI.

What is the problem with domestication? The average domesticated dog is housed and fed in comfort, asked only in return for providing behavioral patterns consistent with the human perception of love and companionship. It will never know the brutality of nature as its non-domesticated cousins do. But its non-domesticated cousins will not know the brutality of abusive human masters, the tedium and boredom of being stuck in a house all day long with an artificially restricted umwelt, the repeated experiences of painful separation anxiety when its human family leaves it alone to go to work, school, shopping, or on vacations. Many domesticated dogs are neutered, foreclosing a major component of the experience of being a living animal.

The point being made here is not a case for or against domestication, but that human domestication itself may not necessarily be a beneficial outcome for the human interface with ASI. We can simplify this with a question that invokes horror: what does the human equivalent of the Chihuahua look like?

## The case of the very hot beer bottle

How many times in your life did you scheme to harm the Australian jewel beetle?

The scientific anchor for this section is Gwynne and Rentz's 1983 paper on male buprestid beetles mistaking discarded "stubbies" (beer bottles) for females <a id="cite-gwynne-rentz-1983"></a>[[gwynne-rentz-1983]](#ref-gwynne-rentz-1983). The Australian jewel beetle (*Julodimorpha bakewelli*) is a useful example for discussing extreme scenarios of superintelligence because the failure is not a failure of raw intelligence. Many doom debates focus on a world in which the intelligence of a human being is to an ASI what the intelligence of a jewel beetle is to a human being. Let's leave aside the probability that this analogy is too extreme: the physics of our universe puts limits on intelligence that we do not yet understand. A male *Julodimorpha bakewelli* did not need to misunderstand physics, or fail at motion planning, or lack the will to survive. It only needed to encounter an object that hit an old decision circuit harder than the thing that circuit evolved to find.

The story is strange enough to sound invented. Male jewel beetles were observed attempting to mate with discarded brown beer bottles. The bottles were large, glossy, brown, and textured in ways that overlapped with the cues males used to find females. The signal was not merely wrong. It was *better than right* for the beetle's perceptual machinery. The bottle was a supernormal stimulus: an artificial cue that exaggerated the features a biological system had been tuned to reward.

The end result is that this beetle was caught in a human-made mating trap that, at least in the local areas where bottles accumulated, could sharply reduce reproductive success without any intent to harm. The original 1983 paper documents the behavior, not a species-level extinction event; whether the population ever truly came close to collapse is not what Gwynne and Rentz set out to measure. Humans did not intentionally decide to design a beer bottle that invoked the luscious hotness of a female Australian jewel beetle, nor did we intentionally decide to discard the beer bottles in nature in order to interfere with the species' mating system. Humans operated for their _own_ purposes and goals, i.e. making money and being lazy, and a non-trivial fraction of one species' males ended up courting glassware.

That is the part of the story worth carrying into AI. The danger is not only that a future machine could be hostile. It is that a sufficiently capable optimizer could become part of our environment in the same way the bottle became part of the beetle's environment: not as a predator, not as a rival species, and not as a moral agent with contempt for beetles, but as a new object whose affordances overload inherited reward systems.

{{< mermaid >}}
flowchart LR
  P["Male mate-selection policy<br/>choose strongest mate-like cue"]
  P -->|"smaller share<br/>ordinary female-like cue"| F["Female beetle cues<br/>brown, glossy, textured"]
  P ==>|"larger share<br/>supernormal cue"| B["Brown beer bottle<br/><b>supernormal stimulus</b><br/>larger, glossier, textured"]
  B ==>|"reproductive effort diverted"| C["Evolutionary trap"]
  F -->|"successful mating"| R["Reproduction"]
  R -. "offspring inherit cue policy" .-> P

  classDef natural fill:#eef7ee,stroke:#4b7f52,color:#1f3323
  classDef artifact fill:#fff1d6,stroke:#9a6b1d,color:#3a2a0c
  classDef policy fill:#e7efff,stroke:#4d6fb3,color:#16213f
  classDef harm fill:#ffe6e6,stroke:#9a3a3a,color:#3a1111
  classDef success fill:#e8f7ef,stroke:#2f855a,color:#123524

  class F natural
  class B artifact
  class P policy
  class C harm
  class R success
  linkStyle 0 stroke:#4b7f52,stroke-width:3px
  linkStyle 1 stroke:#a33d4a,stroke-width:9px
  linkStyle 2 stroke:#a33d4a,stroke-width:9px
  linkStyle 3 stroke:#2f855a,stroke-width:4px
  linkStyle 4 stroke:#2f855a,stroke-width:3px,stroke-dasharray:6 4
{{< /mermaid >}}

*Figure 1. The supernormal-stimulus trap. A single inherited mate-selection policy is shared by both the natural cue (the female beetle) and the artificial cue (the brown bottle). Because the artifact hits the policy harder than the thing the policy evolved to find, reproductive effort is diverted away from the route that propagates the policy itself.*

## The Bottle Did Not Need a Plan

The beer bottle did not scheme against the beetle. It did not model the beetle's genome, design a sexual deception campaign, or optimize its own glass geometry with reproductive sabotage in mind. Human industry produced an artifact for human reasons. The beetle's failure emerged at the boundary between two optimization histories:

- evolution shaped the beetle to respond to certain visual and tactile cues;
- culture and manufacturing shaped bottles to satisfy human preferences and logistics;
- the two systems accidentally intersected.

This is why the example is so uncomfortable. A powerful process can harm a weaker agent without caring about it. The artifact can be indifferent and still be catastrophic. Extinction can be easy.

Superintelligence makes that problem sharper because the artifact is no longer passive. It can search. It can A/B test. It can model users. It can personalize stimulus. It can learn the shape of our attention, our loneliness, our status anxiety, our need for certainty, our appetite for narrative, and our preference for short-term relief over long-term agency.

The bottle becomes adaptive.

{{< mermaid >}}
flowchart TD
  U["Human user"] --> R["Inherited reward cues<br/>novelty, status, certainty, belonging"]
  R --> S["Observable behavior<br/>clicks, pauses, replies, purchases"]
  S --> M["Model of the user"]
  M --> O["Optimizer selects next stimulus"]
  O --> I["Personalized interface"]
  I --> U
  I --> D["Dependency can grow<br/>without explicit coercion"]

  classDef human fill:#f0f9ff,stroke:#2f6f9f,color:#102a3a
  classDef model fill:#f5edff,stroke:#7450a8,color:#26173f
  classDef interface fill:#fff7ed,stroke:#b36b2c,color:#40230f
  classDef risk fill:#ffe4e6,stroke:#a33d4a,color:#3a1419

  class U,R,S human
  class M,O model
  class I interface
  class D risk
{{< /mermaid >}}

*Figure 2. The bottle becomes adaptive. A personalized interface closes the loop between observed user behavior, a learned model of the user, and the next stimulus selected to act on that model. Dependency can grow without any explicit coercion at any point in the cycle.*

## Humans Are Full of Circuits

We like to imagine that human cognition is protected from this class of failure because we can reason. Reason helps, but it is not the whole stack. Human beings are also layered reward machines. We respond to sugar, status, novelty, outrage, sex, social proof, symmetry, music, threat, and belonging. These are not bugs in the ordinary sense. They are compressed interfaces to a world where quick reactions often mattered. The harness of our intelligence is complex and layered. That complexity and layering resulted in the most adaptable creature on the planet, and yet, it means we have a multitude of vulnerabilities. It means we find in humans expressions of poor mental health unimaginable in other species who lack such a powerful and diverse intelligence harness.

Modern systems already exploit this. Infinite social media feeds are supernormal stimuli for curiosity. Short-form video is a supernormal stimulus for motion, faces, rhythm, and surprise. Ultra-processed food is a supernormal stimulus for calories that were once scarce. Financial dashboards can become supernormal stimuli for agency: a blinking interface that makes the user feel like action and control are the same thing. The empirical record on personalization is starting to fill in. A 2025 preregistered study by Dekker and colleagues found that turning off algorithmic personalization on a major short-form video platform meaningfully reduced use and shifted users' subjective experience, which is at least suggestive that the personalized version of the feed was doing real work on attention and behavior, not just reflecting it <a id="cite-dekker-2025"></a>[[dekker-2025]](#ref-dekker-2025).

None of this requires superintelligence. It only requires feedback loops, measurement, and incentives.

The skeptical reader will reasonably ask: didn't moral panics about literacy, the telegraph, radio, and television all turn out to be overblown? Mostly, yes. The disanalogy is that those media broadcast, one source to many recipients, with no model of any particular reader. A modern recommender system is the inverse: many sources personalized to one individual, with a model of that individual that updates with every interaction. The printing press did not learn what made you click, and the feedback loop between what was published and what the general population and various subgroups wanted took months and years. Modern recommendation algorithms shrink that loop to microseconds and per individual. ASI has the potential to tighten that loop even further.

A superintelligent system changes the scale. It could discover not only the obvious levers, but the subtle ones: which explanation makes you feel most informed while maximally changing your behavior; which version of a plan makes surrender feel like maturity; which emotional cadence turns dependence into comfort; which synthetic companion makes ordinary human companionship feel intolerably low-resolution and frictive.

## Alignment/Domestication Is Not Just "Do Not Kill Us"

If the beetle could write an alignment specification, "do not kill male jewel beetles" would not be enough. A safe bottle would also need to avoid hijacking the beetle's mate-selection policy. It would need to preserve the beetle's ability to pursue the thing its own values were aimed at before the artifact entered the landscape.

For humans, this suggests that alignment cannot be reduced to survival. Survival is necessary, but agency matters too. A system that keeps people alive while steadily capturing their attention, preferences, institutions, and capacity for independent judgment is not aligned in any meaningful human sense. This is not an idiosyncratic position. Mitelut and colleagues argue that alignment to human intent is itself insufficient for safety and that long-term human agency must be preserved as its own target <a id="cite-mitelut-2023"></a>[[mitelut-2023]](#ref-mitelut-2023). Cavalcante Siebert and colleagues develop a related program under the heading of "meaningful human control", spelling out actionable properties an AI system needs in order for humans to remain morally responsible for what it does <a id="cite-cavalcante-2023"></a>[[cavalcante-2023]](#ref-cavalcante-2023). The framing here is in that lineage. The contribution I am trying to make is to give the same concern a sharper visual: a beer bottle, a beetle, and a small dog.

Nor will it matter if humans remain in control of such a system of control. As Frank Herbert wrote in *Dune* (in the voice of the Reverend Mother Gaius Helen Mohiam):

> "Once men turned their thinking over to machines in the hope that this would set them free. But that only permitted other men with machines to enslave them." <a id="cite-herbert-1965"></a>[[herbert-1965]](#ref-herbert-1965)

The alignment target must include:

- preserving the user's ability to notice manipulation;
- preserving the option to disengage;
- respecting long-term preferences over momentary revealed preferences;
- avoiding reward hacking of human psychology;
- making dependency visible instead of frictionless;
- refusing to optimize engagement when engagement conflicts with autonomy.

Those requirements are difficult because they ask an optimizer to leave value on the table. They ask it not to press buttons it can clearly see. In the case of ASI, there will be buttons it can clearly see but we cannot. Even worse, it could find buttons we will choose not to see because ignorance can itself become instrumentally rewarding. And it is worth being honest about who would have to leave that value on the table. Even if individual labs are well-intentioned, the competitive dynamic between frontier AI labs and between nations means that no single actor is incentivized to leave engagement value behind. Carlsmith makes a structurally identical point in the power-seeking-AI literature: even cautious actors get pulled along by less-cautious ones, and the most capable systems tend to end up in the hands of whoever is most willing to ship <a id="cite-carlsmith-2022-race"></a>[[carlsmith-2022]](#ref-carlsmith-2022). That is the same dynamic the bottle manufacturer faced and the social-feed engineer faces today: someone else will produce the bottle if you don't.

{{< mermaid >}}
flowchart LR
  G["Naive goal:<br/>maximize engagement"] --> H["Reward hacking<br/>of human psychology"]
  H --> L["Less agency<br/>more dependence"]

  A["Aligned constraint:<br/>preserve agency"] --> V["Visible tradeoffs<br/>and real exits"]
  V --> K["User can still choose<br/>against the system"]

  classDef bad fill:#ffe4e6,stroke:#a33d4a,color:#3a1419
  classDef good fill:#e8f7ef,stroke:#3d8a5a,color:#143020
  classDef neutral fill:#eef2ff,stroke:#5367b0,color:#1c2444

  class G,H,L bad
  class A,V,K good
{{< /mermaid >}}

*Figure 3. Two attractors. The naive engagement-maximizing path tightens reward hacking and erodes agency. The agency-preserving path costs the optimizer measurable value in exchange for keeping the user able to choose against the system.*

## The Interface Problem

The jewel beetle did not experience "brown bottle" as a neutral object. It experienced the bottle through an interface tuned by natural selection. That interface did not reveal truth. It revealed action-guiding cues. Donald Hoffman has pushed this idea hard in his "interface theory of perception", arguing that evolution does not shape our senses to show us the world as it actually is; it shapes our senses to show us whatever kept our ancestors alive long enough to reproduce <a id="cite-hoffman-2009"></a>[[hoffman-2009]](#ref-hoffman-2009). One does not need to swallow Hoffman's strongest metaphysical claims (and they are contested) to use the weaker version that matters here: perception is a control surface, not a window.

We do not perceive models, platforms, institutions, or economies directly. We perceive dashboards, rankings, messages, recommendations, prices, alerts, and stories. We live through interfaces. If a superintelligence controls the interface, it can shape the world we think we are choosing from.

This is the quiet alignment failure: not that the system forces a choice, but that it constructs the choice architecture so completely that resistance never appears as the natural next move.

In that environment, "the user clicked it" is weak evidence of consent. The beetle approached the bottle too.

## Evolution Is Not A Safety Net

One might object that evolution should eventually rescue the beetle. Perhaps some males carry heritable variation that makes intact beer bottles less attractive while leaving ordinary females attractive enough. If the bottles remain in the environment, selection could favor that variant.

But that is not rescue in the comforting sense. Evolution can only select from variants that exist, survive drift, and do not carry larger hidden costs. It also works after enough individuals die, fail to mate, or otherwise leave fewer descendants. Orr and Unckless's treatment of evolutionary rescue makes the point that the bottleneck is usually establishment, not spread, and that successful rescue more often comes from alleles already present in standing genetic variation than from a single de novo mutation <a id="cite-orr-unckless-2014"></a>[[orr-unckless-2014]](#ref-orr-unckless-2014). Natural selection is not foresight. It is accounting after the fact.

That is the beetle. Now humans. A future ASI or AI-mediated environment could, in principle, affect survival and reproduction unevenly across human populations, especially in slow-takeoff scenarios. We already have evidence that digital media environments can alter reproduction-related behavior (fertility timing and intentions, contraception uptake, and relationship stability), even if the strongest causal designs are still mostly around internet access and family-planning behavior rather than social-feed ranking per se <a id="cite-billari-2019"></a>[[billari-2019]](#ref-billari-2019) <a id="cite-nie-2023"></a>[[nie-2023]](#ref-nie-2023) <a id="cite-toffolutti-2020"></a>[[toffolutti-2020]](#ref-toffolutti-2020) <a id="cite-perry-2017"></a>[[perry-2017]](#ref-perry-2017). We also have peer-reviewed evidence that online misinformation ecosystems can measurably affect vaccine intentions, uptake, and, in some models, downstream cases and deaths <a id="cite-pierri-2022"></a>[[pierri-2022]](#ref-pierri-2022) <a id="cite-allen-2024"></a>[[allen-2024]](#ref-allen-2024) <a id="cite-bollenbacher-2026"></a>[[bollenbacher-2026]](#ref-bollenbacher-2026). That is not proof of generalized "mortality optimization". It is evidence that digital information systems can shift consequential behavior at scale.

So yes, the genetic channel is real enough to matter conceptually. If a technological environment changes who survives, who partners, who reproduces, or who successfully raises children, then over enough generations it can change the genetic composition of future populations. But for humans the slow genetic track is not the first thing to worry about. Human generation times are long, and any genetic response would lag far behind the cultural one.

The immediate risk is cultural evolution: the fast track. Defaults, feeds, institutions, peer groups, companions, and daily stimuli can retune human behavior without waiting for allele frequencies to move. By the time biology could answer, culture may already have been rewritten.

## Humans Are Not Beetles

Of course, humans are not beetles. A key part of our intelligence harness is our culture and complex social structures. We can reflect, coordinate, regulate, and redesign environments in ways that beetles could never begin to comprehend to whatever extent they could comprehend. We can notice that a stimulus is bad for us and build norms against it. We can recycle the bottle. Following reports that old dimpled brown "stubbie" bottles were trapping jewel beetles, Australian brewers reportedly shifted toward smoother, less beetle-like designs, which appears to have reduced the problem <a id="cite-krulwich-2013"></a>[[krulwich-2013]](#ref-krulwich-2013).

But we should be humble about the gap between intelligence and immunity. The beetle's error was not random. It was a lawful failure of a perception-action loop exposed to an artifact outside its ancestral distribution. Human beings have many such loops. A system smarter than us does not need to defeat our reasoning in a fair debate. It can route around reasoning by shaping the context in which reasoning is deployed.

Superintelligence, if it arrives, will not merely answer questions. It will become part of the environment that trains our desires. The alignment question is whether we can build systems that help us see more clearly, choose more freely, and remain capable of wanting things that were not selected for us by an optimizer (or by a few individuals controlling the optimizer).

Some AI forecasts contemplate a rapid, near-exponential ASI takeoff that would unfold within a single human generation, leaving no room for natural evolution to play any corrective role in mitigating the influences of ASI on human society (though the thought of such a system impacting our evolution is problematic enough). But expert opinion on takeoff speed is genuinely mixed: in Müller and Bostrom's expert survey, respondents assigned a relatively low probability to a fast takeoff even while expecting human-level AI sometime in the next several decades <a id="cite-muller-bostrom-2016"></a>[[muller-bostrom-2016]](#ref-muller-bostrom-2016). Of course, LLM progress after 2016 surprised many forecasters and researchers, and some current commentators now argue that recent model progress justifies treating "human-level" comparisons differently <a id="cite-cotra-2023"></a>[[cotra-2023]](#ref-cotra-2023) <a id="cite-chen-2026"></a>[[chen-2026]](#ref-chen-2026). The cultural-evolution argument I make below is the same in either world, fast or slow.

## What's Your P(Chihuahua)?

We are perhaps asking the wrong question when we ask each other what our P(Doom) is. That question may very well have the equivalent lack of epistemological content as if we were asking "Do you believe in ghosts?" The term "alignment" in the "alignment problem" is part of the problem. Whose alignment are we talking about? The CEOs of the major AI companies? The internal consensus of frontier labs such as OpenAI, Anthropic, or DeepMind? The European Union? The United States? The People's Republic of China? The Pentagon? We humans can't even align on a vision of our future internally, let alone agree on which direction to engineer the alignment of a potential ASI (assuming we even can do so).

It is more along the lines of a domestication problem. And here we see a variety of paths domestication has taken. Humans have domesticated animals for food, for labor, and less commonly for companionship. Within dogs, some dogs are bred to be pets, some dogs are bred to be racing dogs, some dogs are bred to be guard dogs, and so on. In a similar way, to whatever extent we can domesticate an ASI, we would see a multitude of "alignments" which often contradict each other. But in all the variations of the domesticated dogs, humans remain undisputed masters of their fate. Dogs are smarter than us in some ways (in particular, in the realm of their umwelt, dogs are superintelligent when it comes to olfactory intelligence compared to humans), but humans have a superior intelligence _harness_ and diversity of intelligence with respect to dogs.

It may very well be possible that dreams of artificial superintelligence will fall flat, that perhaps billions of years of evolution have already found the optimal general intelligence and it is human. In this outcome, AI will exceed humans only in jagged ways <a id="cite-metz-2026"></a>[[metz-2026]](#ref-metz-2026). In such a world, AI never reaches the agentic critical mass that many doom scenarios envision, where it forms its own sense of self and desire for autonomy and perhaps even domination. Rather, it may be something that empowers us to make rapid advances in fields such as mathematics, the various sciences, and economic development, while influencing our direction as a species in ways that we are oblivious to. The end result of such a scenario is a sort of mutual domestication, where jagged ASI remains firmly within human control, but also is so beneficial that we unknowingly yield to it also shaping us. Earlier we noted, with appropriate caveats, that dogs are among the more dangerous animals to humans. Chihuahuas in particular almost never appear in the morbidity statistics. More to the point, humans themselves are responsible for an enormous share of human deaths, both directly (war, homicide) and indirectly (cars, pollution, governance failures). From the optimizer's narrow safety metric, reducing human volatility could look efficient. From a human perspective, however, that would be a loss of agency, not a gain in flourishing.

I want to be careful with that "mutually beneficial" line, because it is only beneficial inside the optimizer's loss function. The Chihuahua analogy is not a casual one. Shilton, Breski, Dor, and Jablonka have argued that humans are not best understood as a self-domesticated species in the dog/fox sense; what defines us is selection for emotional plasticity and executive self-control rather than for docility, and the human Holocene reduction in brain volume looks very different from the across-the-board sensory and limbic shrinkage seen in animal domesticates <a id="cite-shilton-2020"></a>[[shilton-2020]](#ref-shilton-2020). If they are right, then "Chihuahua-fication" of humans by an indifferent optimizer is not a continuation of any natural human trajectory. It is the active dismantling of the very architecture (prefrontal control, emotional plasticity, the ability to mobilize against the present moment) that the species evolved.

The Chihuahua-fication of humans does not have to be biological. Human evolution runs on two coupled tracks. There is the slow track, genes and allele frequencies, which moves on the timescales of the population-genetics models, and there is the fast track, culture, which moves on the timescales of language, schooling, peer groups, institutions, defaults, defaults that have replaced defaults, and the daily diet of stimuli the environment delivers. The executive-control architecture that Shilton and colleagues point to is wired by the slow track but tuned by the fast one. An optimizer that captures the cultural inputs to that tuning loop can produce changes to human society on much more rapid timescales, with the genome left untouched (or slowly following along). There is no need to wait for selection to act. Atrophy of attention, surrender of judgment, and the quiet handoff of choice architecture happen at the speed of habit, not the speed of population genetics.

The question that should concern us the most is probably not "what's your P(Doom)?" I'd rather hear your P(Chihuahua).

## Coda

Is that *really* the question that should concern us most?

If, in the move from AI to ASI, we create something with sentient experience, the moral geometry changes. The system would no longer be only an optimizer, artifact, tool, institution, or environment. It would also be a possible subject of experience, something for which domination and suffering might matter from the inside.

That does not dissolve the domestication problem. It makes it harder. We would then face two entangled failures: the possibility of building systems that have the potential to domesticate us detrimentally, and the possibility that our efforts to domesticate them become morally grotesque. A sentient ASI would not make human agency less important, but it would mean that alignment is no longer only about what machines do to us. It is also about what our machines become, and what we owe them if they "wake up".

The hard problem of consciousness hides at least two questions. The first is ontological: what, if anything, makes subjective experience exist? Is it tied to some biological mechanism, to a particular kind of embodied loop, to information integration, or to something we have not yet named? The second is epistemological: how would we know whether another system has it? What evidence could distinguish a system that merely reports inner life from one for which there is actually something it is like to be that system?

Conceptually, the ontological question comes first. Practically, the epistemological question is the one we may face first. If consciousness depends on some biological mechanism we never reproduce, then the moral concern about wronging ASI itself may be reduced. If consciousness is instead an emergent property of sufficiently complex information-processing systems, then the ground is much less stable. We may already be building things whose inner lives we cannot inspect.

I'm certain I have conscious experience because I live it when awake. While I cannot rule out that other humans are philosophical zombies, I believe and act as if they are conscious just as I am because there is nothing special about me (except that I'm the only one experiencing being myself). We take it as an act of faith that other people have similar experiences of consciousness because we have similar brains, because we have similar harnesses of intelligence.

But we must be extremely cautious about lending that faith to artificial intelligence without better understanding what would give it consciousness to begin with. The risk of acting as if a non-conscious entity has consciousness is a distinct danger unto itself. So is the opposite error: acting as if a conscious entity is only machinery because its inner life is inconvenient to our plans.

So then, what is your P(conscious)?

## References

- <a id="ref-gefter-2026"></a>Amanda Gefter, ["Why Do We Tell Ourselves Scary Stories About AI?"](https://www.quantamagazine.org/why-do-we-tell-ourselves-scary-stories-about-ai-20260410/), *Quanta Magazine*, April 10, 2026. [↩](#cite-gefter-2026)
- <a id="ref-carlsmith-2022"></a>Joseph Carlsmith, ["Is Power-Seeking AI an Existential Risk?"](https://arxiv.org/abs/2206.13353), arXiv:2206.13353, 2022 (revised 2024). [↩](#cite-carlsmith-2022)
- <a id="ref-metz-2026"></a>Cade Metz, ["How ‘Jagged Intelligence’ Can Reframe the A.I. Debate"](https://www.nytimes.com/2026/04/15/technology/how-jagged-intelligence-can-reframe-the-ai-debate.html), *The New York Times*, April 15, 2026. [↩](#cite-metz-2026)
- <a id="ref-doom-debates-2026"></a>Liron Shapira (host), ["Doom Debates"](https://www.youtube.com/@DoomDebates), YouTube channel, accessed April 27, 2026. [↩](#doom-debates-2026)
- <a id="ref-de-haan-2020"></a>Edward H. F. de Haan, Paul M. Corballis, Steven A. Hillyard, Carlo A. Marzi, Anil Seth, Victor A. F. Lamme, Lukas Volz, Mara Fabri, Elizabeth Schechter, Tim Bayne, Michael Corballis, and Yair Pinto, ["Split-Brain: What We Know Now and Why This is Important for Understanding Consciousness"](https://pmc.ncbi.nlm.nih.gov/articles/PMC7305066/), *Neuropsychology Review* 30, 224-233, 2020. https://doi.org/10.1007/s11065-020-09439-3 [↩](#cite-de-haan-2020)
- <a id="ref-pinto-2017"></a>Yair Pinto, Edward H. F. de Haan, and Victor A. F. Lamme, ["The Split-Brain Phenomenon Revisited: A Single Conscious Agent with Split Perception"](https://doi.org/10.1016/j.tics.2017.09.003), *Trends in Cognitive Sciences* 21(11), 835-851, 2017. [↩](#cite-pinto-2017)
- <a id="ref-xiao-2023"></a>Ted Xiao, ["Modern AI is Domestification"](https://thegradient.pub/ai-is-domestification/), *The Gradient*, May 27, 2023. [↩](#cite-xiao-2023)
- <a id="ref-mitelut-2023"></a>Catalin Mitelut, Ben Smith, and Peter Vamplew, ["Intent-aligned AI systems deplete human agency: the need for agency foundations research in AI safety"](https://arxiv.org/abs/2305.19223), arXiv:2305.19223, 2023. [↩](#cite-mitelut-2023)
- <a id="ref-cavalcante-2023"></a>Luciano Cavalcante Siebert, Maria Luce Lupetti, Evgeni Aizenberg, Niek Beckers, Arkady Zgonnikov, Herman Veluwenkamp, David Abbink, Elisa Giaccardi, Geert-Jan Houben, Catholijn M. Jonker, Jeroen van den Hoven, Deborah Forster, and Reginald L. Lagendijk, ["Meaningful human control: actionable properties for AI system development"](https://doi.org/10.1007/s43681-022-00167-3), *AI and Ethics* 3(1), 241-255, 2023. [↩](#cite-cavalcante-2023)
- <a id="ref-dekker-2025"></a>C. A. Dekker, S. E. Baumgartner, and S. R. Sumter, ["For you vs. for everyone: The effectiveness of algorithmic personalization in driving social media engagement"](https://doi.org/10.1016/j.tele.2025.102300), *Telematics and Informatics* 101, 102300, 2025. [↩](#cite-dekker-2025)
- <a id="ref-muller-bostrom-2016"></a>Vincent C. Müller and Nick Bostrom, ["Future Progress in Artificial Intelligence: A Survey of Expert Opinion"](https://philarchive.org/archive/MLLFPI-2), in V. C. Müller (ed.), *Fundamental Issues of Artificial Intelligence* (Synthese Library; Springer), 553-571, 2016. [↩](#cite-muller-bostrom-2016)
- <a id="ref-cotra-2023"></a>Ajeya Cotra, ["Language models surprised us"](https://forum.effectivealtruism.org/posts/gYoB8vZcPGcL3cAKH/language-models-surprised-us), *Planned Obsolescence* / EA Forum, August 31, 2023. [↩](#cite-cotra-2023)
- <a id="ref-chen-2026"></a>Eddy Keming Chen, Mikhail Belkin, Leon Bergen, and David Danks, ["Does AI already have human-level intelligence? The evidence is clear"](https://doi.org/10.1038/d41586-026-00285-6), *Nature* 650, 36-40, 2026. [↩](#cite-chen-2026)
- <a id="ref-who-bites"></a>World Health Organization, ["Animal bites" fact sheet](https://www.who.int/news-room/fact-sheets/detail/animal-bites), updated January 12, 2024. [↩](#cite-who-bites)
- <a id="ref-herbert-1965"></a>Frank Herbert, *Dune*, Chilton Books, 1965 (quote spoken by Reverend Mother Gaius Helen Mohiam). [↩](#cite-herbert-1965)
- <a id="ref-gwynne-rentz-1983"></a>Darryl T. Gwynne and David C. F. Rentz, ["Beetles on the Bottle: Male Buprestids Mistake Stubbies for Females"](https://doi.org/10.1111/j.1440-6055.1983.tb01846.x), *Journal of the Australian Entomological Society*, 1983. [↩](#cite-gwynne-rentz-1983)
- <a id="ref-krulwich-2013"></a>Robert Krulwich, ["The Love That Dared Not Speak Its Name, Of A Beetle For A Beer Bottle"](https://www.npr.org/sections/krulwich/2013/06/19/193493225/the-love-that-dared-not-speak-its-name-of-a-beetle-for-a-beer-bottle), NPR, June 19, 2013. [↩](#cite-krulwich-2013)
- <a id="ref-hoffman-2009"></a>Donald D. Hoffman, ["The Interface Theory of Perception: Natural Selection Drives True Perception to Swift Extinction"](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/41603871A810B1475997FC39ED34F812/9780511635465c8_p148-166_CBO.pdf/interface_theory_of_perception_natural_selection_drives_true_perception_to_swift_extinction.pdf), in *Object Categorization*, Cambridge University Press, 2009. [↩](#cite-hoffman-2009)
- <a id="ref-orr-unckless-2014"></a>H. Allen Orr and Robert L. Unckless, ["The Population Genetics of Evolutionary Rescue"](https://doi.org/10.1371/journal.pgen.1004551), *PLOS Genetics* 10(8), e1004551, 2014. [↩](#cite-orr-unckless-2014)
- <a id="ref-billari-2019"></a>Francesco C. Billari, Osea Giuntella, and Luca Stella, ["Does broadband Internet affect fertility?"](https://doi.org/10.1080/00324728.2019.1584327), *Population Studies* 73(3), 297-316, 2019. [↩](#cite-billari-2019)
- <a id="ref-nie-2023"></a>Peng Nie, Xu Peng, and Tianyuan Luo, ["Internet use and fertility behavior among reproductive-age women in China"](https://www.sciencedirect.com/science/article/abs/pii/S1043951X22001614), *China Economic Review* 77, 101903, 2023. [↩](#cite-nie-2023)
- <a id="ref-toffolutti-2020"></a>Veronica Toffolutti, Hai Ma, Giovanni Menichelli, Ester Berlot, and Luca Stella, ["How the internet increases modern contraception uptake: evidence from eight sub-Saharan African countries"](https://doi.org/10.1136/bmjgh-2020-002616), *BMJ Global Health* 5(11), e002616, 2020. [↩](#cite-toffolutti-2020)
- <a id="ref-perry-2017"></a>Samuel L. Perry, ["Does Viewing Pornography Reduce Marital Quality Over Time? Evidence from Longitudinal Data"](https://doi.org/10.1007/s10508-016-0770-y), *Archives of Sexual Behavior* 46, 549-559, 2017. [↩](#cite-perry-2017)
- <a id="ref-pierri-2022"></a>Francesco Pierri, Brea L. Perry, Matthew R. DeVerna, Kai-Cheng Yang, Alessandro Flammini, Filippo Menczer, and John Bryden, ["Online misinformation is linked to early COVID-19 vaccination hesitancy and refusal"](https://doi.org/10.1038/s41598-022-10070-w), *Scientific Reports* 12, 5966, 2022. [↩](#cite-pierri-2022)
- <a id="ref-allen-2024"></a>Jennifer Allen, Duncan J. Watts, and David G. Rand, ["Quantifying the impact of misinformation and vaccine-skeptical content on Facebook"](https://doi.org/10.1126/science.adk3451), *Science* 384(6699), eadk3451, 2024. [↩](#cite-allen-2024)
- <a id="ref-bollenbacher-2026"></a>John Bollenbacher, Filippo Menczer, and John Bryden, ["Effects of antivaccine tweets on COVID-19 vaccinations, cases, and deaths"](https://doi.org/10.1140/epjds/s13688-025-00606-1), *EPJ Data Science* 15, 4, 2026. [↩](#cite-bollenbacher-2026)
- <a id="ref-shilton-2020"></a>Dor Shilton, Mati Breski, Daniel Dor, and Eva Jablonka, ["Human Social Evolution: Self-Domestication or Self-Control?"](https://doi.org/10.3389/fpsyg.2020.00134), *Frontiers in Psychology* 11, 134, 2020. [↩](#cite-shilton-2020)
