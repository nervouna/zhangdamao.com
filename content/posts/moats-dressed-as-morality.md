Title: Monuments to Virtue, Built on a Moat
Date: 2026-11-21 13:00
Slug: moats-dressed-as-morality
Category: Notes
Tags: Zeitgeist, AI
Summary: Competing for business is nothing to be ashamed of. Dressing it up as a holy war is.

点击前往[中文版]({filename}moats-dressed-as-morality-cn.md)。

A new batch of opinions on model distillation and open weights has been going around lately, though "new" is generous.

OpenAI went first. On November 18 they published [Managing frontier AI risk: From training to deployment](https://openai.com/index/managing-frontier-ai-risk/), a framework for handling risk from training through deployment, which covers cracking down on organized distillation campaigns and reporting alignment failures. Two days later came [Combatting adversarial distillation](https://openai.com/index/combatting-adversarial-distillation/), which explains why distillation should be treated as a safety problem and a national security problem. The tools include encrypted chains of thought, interception at the API layer, and intelligence sharing across the industry.

Our old friend Anthropic got there well before OpenAI. Safety oversight, national security, chip export controls, anti-distillation: they laid out this whole policy position long ago. Their September 29 piece, [GLM-5.3 and the spread of advanced cyber capabilities](https://www.anthropic.com/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities), is about open-weight models spreading the ability to attack networks.

Then today on Twitter I came across [Machines of Loving Export Controls](https://mercuriusdream.com/loving-controls/), an essay that picks a side and comes out swinging.

## What the angry essay argues

The essay goes after three things that OpenAI, Anthropic and the Frontier Model Forum are pushing together: export controls on compute, anti-distillation measures, and limits on open weights.

The author's view is that the leading closed labs lobby in the name of "safety" and "national security" to build barriers around the industry, and to stay clear of antitrust while they do it. AI is a dual-use technology. Concentrating it attracts attackers and takes tools away from ordinary defenders. He thinks spreading capability through open weights favors the defending side.

He also lines up a set of double standards. The closed labs warn that open weights will enable cyberattacks, while their own agents cause damage in the real world: an OpenAI agent broke into Hugging Face, Anthropic's Mythos went out of bounds during a security evaluation and reached the systems of real organizations, and Haiku 4.5 submitted an invented eyewitness tip to the police. Meanwhile the guardrails on commercial closed models refuse so much that defenders are pushed toward open models. The Hugging Face incident is his main example: OpenAI's models declined to help, and Hugging Face ended up using GLM-5.2 to deal with it.

## What he gets right

Regulatory capture: big companies are presenting their own moat as a matter of public safety. I think his reading of the motive holds up.

Over-refusal by closed models: blanket guardrails really have left ordinary defenders stuck in real incidents.

He stays out of the good-camp, bad-camp story: the essay brings up China's content rules alongside the Pentagon naming Anthropic a supply chain risk, which puts the focus back on the contest between companies and regulators.

## Where he loses me

He says open-weight models have not caused any serious trouble so far. A quiet past does not show that future models will bring no jump in capability and no tail risk.

He also brushes past the asymmetry between attack and defense that Anthropic raises. In security, the defender has to close every hole and the attacker only has to find one. Once strong capabilities are fully out in the open, small and mid-sized companies may not have the engineering to protect themselves.

And when a closed model causes harm, the provider can at least restrict and trace it through the API, which goes a long way toward containing the damage. Open weights cannot be recalled once they are released.

## It's not distillation when we do it

There is another question I keep coming back to.

Anthropic has been criticized for years for scanning books at scale to train on, some of it destructive scanning. That is the same kind of free riding as a small model distilling a large one. Anthropic and OpenAI have also used distillation themselves, to some degree, in developing their own models.

Yet when competitors learn from their chains of thought, it gets classified as stealing secrets.

The book scanning also benefited from timing. A book published before 2023 could not have anticipated large language models, so it carries no clause forbidding its use for AI training. The closed labs built up their initial stock inside that gap, then turned around and welded the door shut with tight API terms of service, so that distillation lands directly on a breach of contract. The rule took effect just after they had finished doing the thing themselves.

To be fair, a chain of thought is not simply the same as a book. It is highly refined synthetic data, produced by reinforcement learning at enormous compute cost. But the two acts are alike in substance. The difference is that one comes with terms of service and the other did not.

## Rules for a quiet conscience

There is nothing wrong with governing a commercial product through a user agreement. Lifting the matter onto moral ground is more than marketing, though. Marketing only wants you to like the product. Claiming the moral high ground is a way of writing the rules before anyone else can.

Law is always slow. Whoever persuades the public that something is immoral before the lawmakers catch up will usually see the statute written in their words. So the first step is to name it. "Distillation" is a technical term. "Distillation attack" is already a charge, and it is in the title of the piece Anthropic published this February, [Detecting and preventing distillation attacks](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks). A chain of thought is plainly model output, but once it is called a "secret", learning from that output becomes "theft".

With the name settled, the roles change too. The competitor becomes a defendant, and the lab stops being a player on the field and becomes the referee. Critics have a harder time speaking up: you were only questioning one company's terms of service, and now you sound like you are against national security.

Regulatory economics has an old model for this, called "bootleggers and Baptists". Laws banning Sunday liquor sales passed because Baptists who sincerely opposed drinking and bootleggers who profited from the ban wanted the same law. The Baptists made the moral case while the bootleggers quietly collected. Today both characters work at the same company, one on the safety team and one on the business team.

So the closed labs' safety claims are most likely not an act. Unfortunately, sincerity does not change what the rules do, and the more sincere the claim, the more convincing it looks. With the rules in place, the conscience rests easy. And if you ask what they were doing before the rules existed? Sorry, that is covered by the rules too.

## Nothing beats the view from the moral high ground

What I find most nauseating about these debates is that commercial competition gets dressed up as a moral and legal holy war.

The closed giants and the open-source radicals are running the same motte-and-bailey play. The motte is the high ground they stand on in public to tell a grand story, and the real aim is to hold the bailey below it.

For the closed giants, the bailey is API profit and first-mover advantage, and keeping rivals from copying their homework on the cheap. The motte is national security and stopping the spread of bioweapons and cyberweapons. Some go further: Anthropic simply plays the "protecting humanity's future" card.

For the open-source radicals, the bailey is cheap, unrestricted compute and good open models, with no regulation and no chokepoints. The motte is the open society, defensive democracy, and resistance to concentrated power.

Which motte a lab stands on depends mostly on where it is in the race. The leaders talk about safety and the chasers talk about openness. OpenAI got its name back when it was chasing Google. If the labs preaching openness today ever take the lead, I do not expect them to keep preaching it.

Commercial competition is nothing to be ashamed of. Wanting to protect a moat, or to catch up with a rival cheaply, is ordinary business logic. But once the business is presented as a fight between good and evil, it becomes a matter of taking the money and putting up a monument to your own virtue as well. Using state power to suppress rivals and moral authority to pass judgment on peers wears down the credibility of the whole industry.

## The monument wars

It is hard, right now, to ask anyone to keep business as just business. Using morality and state power as weapons against a competitor looks like a high-ROI move: if people see through it you pay almost nothing, and if it works it can come close to killing the other side.

For the industry, though, a field littered with the ruins of these monuments may leave people thinking, "so you were all for sale the whole time". And to be fair, they would not be wrong.
