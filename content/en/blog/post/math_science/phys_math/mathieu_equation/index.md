---
title: "Quantum Computers:  Mathieu's Equations and the Quadrupole Ion Traps"
authors: ["t-jones"]
date: "2024-08-17"
draft: false
categories:
  - deep-dive
  - physics
tags:
  - physics
  - math
  - quantum-computers
math: true
summary: Of great use to physics, including one of the promising paths towards quantum computers, is the ion trap. Though there are various models in use, we focus here on Paul-style models. To do so, we need to understand Mathieu's equations and their corresponding solutions in enough detail to grasp the function of the Paul ion trap. In this report, we explore the behavior of Mathieu's equation and its solutions for the Paul ion trap.
resources:
    image: "sor_diagram.png"
---

In order to conduct quantum-mechanics-oriented experiments or operate ion-trap-based quantum computers, 
we need a way to manipulate small particles. For example, if we want to observe the 
behavior of an ion when we hit it with lasers of a certain frequency, we will need to keep it confined in a small area. How can we do so?

To get _closer_ to understanding the answer takes us through some rougher-than-usual (for a blog post) mathematical woods, but anyone spending enough time with mathematics knows that difficult journeys are often rewarded with beauty. Look at the image below, one we will earn the right to admire not just aesthetically,
but also mathematically. This image answers the question of how we can keep ions trapped, and this post will outline the mathematical reason why this answer is found in something so unexpectedly interesting.

{{< figure src="peak.png" width="100%">}}


## What is the Quadrupole Ion Trap (AKA the RF Paul ion trap)?

One way to confine an atomic ion is to provide a force of the form \\(F = -kr\\). 
What would this entail for an electrical potential? Since the electric field is proportional to the force, and is equal to the negative gradient of the potential, 
we might use an electric potential of the form:

$$\Phi \propto (\alpha x^2 + \beta y^2 + \gamma z^2)$$

That is, we require an electric quadrupole field. 

This equation must obey the condition imposed on all electric potentials where there is no free charge distribution, namely Laplace's equation:

$$\nabla^2\Phi = 0 \rightarrow \alpha + \beta + \gamma = 0$$

We can satisfy this in more than one way. For the linear Paul trap, whose initial manifestations were not as a 
trap but as a focusing tunnel of sorts, but which can be turned into a 'race track' ion trap:

{{< alert title="The Linear Paul Trap" color="primary" >}}
$$\alpha = 1 = -\gamma, \beta = 0 \rightarrow \Phi = \frac{\Phi_0}{2r_0^2}(x^2 - z^2)$$
{{< /alert >}}

For the true 3D rf Paul trap (the "ionenkäfig" or chamber trap) that restrains ions in all three dimensions:

{{< alert title="The 3D Chamber Trap (Ionenkäfig)" color="primary" >}}
$$\alpha = \beta = 1, \gamma = -2 \rightarrow \Phi = \frac{\Phi_0}{2r_0^2}(x^2 + y^2 - 2z^2)$$
{{< /alert >}}

This figure (from reference <a id="cite-paul-1990"></a>[[paul-1990]](#ref-paul-1990)) shows a diagram of an idealized rf Paul trap (a) and the chamber rf Paul trap (b):


{{< figure src="rf_paul_trap_diagram.png" caption="The linear rf Paul trap (a) and the chamber rf Paul trap (b). Figure from ref. [[paul-1990]](#ref-paul-1990).">}}

Such potentials can be provided via hyperbolic-shaped electrodes. We can perform a successive over-relaxation (SOR) of a cross section of these electrodes and find that indeed a two-dimensional stable equilibrium is created at the center (though this is unstable in the third dimension, z) when we satisfy the above conditions (focusing on the chamber trap):

{{< figure  src="sor_diagram2.png" caption="SOR calculation for hyperbolic electrodes. The outer box is held at ground, the horizontal electrodes held at V and the vertical ones held at -V. The grid was 1000 by 1000, our tolerance was 0.0001.">}} 

We have a repulsive force in the \\(z\\) direction which must be avoided. Unfortunately, [Earnshaw's theorem](https://en.wikipedia.org/wiki/Earnshaw%27s_theorem) tells us that it isn't possible to make an electric potential whose result is a stable equilibrium confining in all three dimensions of space using only *static* inverse-square forces. However, we can create a potential which results in an *average* confining force by using time-dependent fields. This can be done via the clever mechanism of rotating the field so that the focusing and defocusing is applied alternatively in each direction. If done at the right set of frequencies, the ion will maintain a stable orbit near the center of the ion trap.

{{< figure  src="hyperbolic_electrodes_with_field.gif" caption="Animation of field rotation.">}} 


A way to visualize this is with W. Paul's mechanical analog <a id="cite-paul-1990"></a>[[paul-1990]](#ref-paul-1990), <a id="cite-thompson-2002"></a>[[thompson-2002]](#ref-thompson-2002). Paul made an equivalent potential as that described above by carving a hyperbolic saddle surface out of plexiglass. Placing a ball on top of this surface would result in the ball falling off, of course. But if the surface is rotated at a proper rate, the ball will stay on the surface.

{{< figure src="saddle_figure.png" caption="The mechanical analog to the rf Paul trap; the ball will fall off unless the saddle rotates fast enough that in any given direction there is an alternation of force direction over the cycle of rotation.">}} 

<!-- ![Figure 1.3: The mechanical analog to the rf Paul trap](saddle_figure.png) -->

{{< alert title="A note on traps" color="warning" >}}
This post will derive the Mathieu stability equations for a *pure 3D quadrupole rf field*. In a **linear trap** (often utilized for Quantum Computing hardware), the axial confinement along \\(z\\) is typically DC (static harmonic)—not Mathieu in the same way—and the Mathieu stability chart we derive predominantly governs only the radial \\(x,y\\) directions. Conversely, the classic 3D "chamber" trap relies upon true 3D rf confinement, which we model below.
{{< /alert >}}

The applied oscillating potential can be written:

$$\Phi_0 = U + V \cos \Omega t$$

If the particle has a charge \\(e\\) and mass \\(m\\), the resulting electric field is \\( \mathbf{E} = -\nabla \Phi \\):

$$
\mathbf{E} = -\frac{U + V \cos \Omega t}{r_0^2} (x \mathbf{\hat{i}} + y \mathbf{\hat{j}} - 2z \mathbf{\hat{k}})
$$

This gives us the coordinate-wise equations of motion:

$$
\begin{align*}
\ddot{x} + \frac{e}{mr_0^2}(U + V \cos \Omega t)x &= 0 \\\\
\ddot{y} + \frac{e}{mr_0^2}(U + V \cos \Omega t)y &= 0 \\\\
\ddot{z} - \frac{2e}{mr_0^2}(U + V \cos \Omega t)z &= 0
\end{align*}
$$


These equations can be cast as Mathieu's equation, which describes the parametric resonance driving the ion's stability:

$$\ddot{\eta} + \left(a - 2q \cos(2\tau)\right)\eta = 0$$

The variables are dimensionless for this equation, so we have a little work to do to massage our motion equations into this form.

{{< alert title="Mapping Coordinates to Mathieu Parameters" color="info" >}}

Since we are removing dimensionality in the \\(t\\) variable by setting \\( \tau = \Omega t / 2\\),

$$ \ddot{\eta} = \frac{\Omega^2}{4}\frac{d^2\eta}{d\tau^2} $$

For the \\( x \\) and \\(y\\)-directions, the equation of motion:

$$\ddot{x} + \frac{e}{mr_0^2}(U + V \cos \Omega t)x = 0$$

can be rewritten by defining:

$$
a_x = a_y = \frac{4eU}{mr_0^2\Omega^2}, \quad q_x = q_y = -\frac{2eV}{mr_0^2\Omega^2}, \quad \tau = \frac{\Omega t}{2}
$$

resulting in the Mathieu equation form:

$$\frac{d^2x}{d\tau^2} + \left(a_x - 2q_x \cos(2\tau)\right)x = 0$$

For the \\(z\\)-direction equation of motion:

$$\ddot{z} - \frac{2e}{mr_0^2}(U + V \cos \Omega t)z = 0$$

We similarly define:

$$
a_z = -\frac{8eU}{mr_0^2\Omega^2}, \quad q_z = \frac{4eV}{mr_0^2\Omega^2}
$$

resulting in:

$$\frac{d^2z}{d\tau^2} + \left(a_z - 2q_z \cos(2\tau)\right)z = 0$$

Notice the critical relationship between the stability parameters:

$$ a_z = -2a_x, \qquad q_z = -2q_x $$

As we will see, the general stability diagram for Mathieu's equation is symmetrical upon reflection around \\(q = 0 \\), but _not_ around \\(a = 0\\).
Thus, to find regions of overall 3D stability where the ion is trapped in all directions simultaneously, we must find an operating point \\( (a_x, q_x) \\) such that both \\( (a_x, q_x) \\) and \\( (a_z, q_z) = (-2a_x, -2q_x) \\) lie within stable regions of the generic Mathieu chart.
{{< /alert >}}

##  Mathieu's Equation, solution, and stability

### Basics and Floquet's Theorem

Our derivation below can be found in greater detail and better form in many references <a id="cite-arscott-1964"></a>[[arscott-1964]](#ref-arscott-1964), <a id="cite-mclachlan-1947"></a>[[mclachlan-1947]](#ref-mclachlan-1947), <a id="cite-strang-2005"></a>[[strang-2005]](#ref-strang-2005), and our derivation follows the spirit of these. An equation such as Mathieu's equation,

{{< alert title="Mathieu's equation" color="secondary" >}}
$$\ddot{\eta} + (a - 2q \cos(2\tau))\eta = 0     $$
{{< /alert >}}

is of a class of differential equations of the type <a id="cite-boyce-1996"></a>[[boyce-1996]](#ref-boyce-1996),

$$L[y] = y^{\prime \prime} + p(t)y^{\prime} + s(t)y = 0     $$

Any two fundamental solutions to this equation, \\(y_1(t), y_2(t)\\), will satisfy the set of boundary value equations,

$$
\begin{align*}
c_1 y_1(t_0) + c_2y_2(t_0) &= y_0 \\\\
c_1 y^{\prime}_1(t_0) + c_2y^{\prime}_2(t_0) &= y^{\prime}_0 
\end{align*}
$$

This equation can be summarized in the matrix equation \\(Y\mathbf{c} = \mathbf{y}\\). We thus require 
that the determinant of Y (called the Wronskian in this context) is not equal to zero (guarantees that the two solutions are linearly independent),

{{< alert title="Wronskian" color="secondary" >}}
$$
W(Y) = \det(Y)  = \begin{vmatrix}
y_1(t_0) & y_2(t_0)\\\\
y^{\prime}_1(t_0) & y^{\prime}_2(t_0)
\end{vmatrix} \neq 0
$$
{{< /alert >}}

The set of even/odd solutions:

$$
\begin{aligned}
y_1 : & \quad y(t_0) = 1, \quad y^{\prime}(t_0) = 0 \\\\
y_2 : & \quad y(t_0) = 0, \quad y^{\prime}(t_0) = 1 \\\\
& \quad \Rightarrow \quad W(Y) = \begin{vmatrix} 1 & 0 \\\\ 0 & 1 \end{vmatrix} = 1
\end{aligned}
$$


are thus fundamental sets of solutions. We may follow Floquet's theorem <a id="cite-arscott-1964"></a>[[arscott-1964]](#ref-arscott-1964), which tells us that Mathieu's equation has at least one solution such that


{{< alert title="Floquet's Theorem" color="secondary" >}}
For a linear differential equation with periodic coefficients, such as \\( y^{\prime\prime} + p(\eta) y = 0 \\), where \\( p(\eta) \\) is periodic with period \\( T \\), the solutions can be written in the form:

$$
y(\eta + T) = \sigma y(\eta)
$$

and so generally:

$$
y(\eta) = e^{i\beta \eta} \phi(\eta), 
$$

where \\( \beta \\) is a constant (often called the characteristic exponent) and \\( \phi(\eta) \\) is a periodic function with the same period \\( T \\) as the coefficients. This form decouples the exponential growth/decay or oscillation from the periodic behavior of the solution. Stable solutions correspond to a real-valued characteristic exponent \\( \beta \in \mathbb{R} \\).

{{< /alert >}}

To help visualize how these mathematical components interconnect, here is an outline of the derivation flow we will follow:

{{< mermaid >}}
flowchart TD
    A["Mathieu's Equation"] --> B["Floquet's Theorem<br>(Assumes quasi-periodic solution)"]
    B --> C["Hill's Method<br>(Fourier Series Expansion)"]
    C --> D["Infinite Determinant Δ(iµ) = 0"]
    D --> E["Whittaker's Approach<br>(Complex Analysis via Liouville's Theorem)"]
    E --> F["Isolates Characteristic Exponent (β)"]
    F --> G["Sträng's Recursion Formula<br>(Calculates Seed Determinant Δ(0))"]
    G --> H["Numerical Stability Diagram Map"]
{{< /mermaid >}}

The details of this process are outlined as follows:

### 2.1b. Floquet's theorem for Mathieu's Equations

To understand how the solutions behave after a shift by the period \\(\pi\\), we examine the following relationships, which stem from the properties of second-order linear differential equations with periodic coefficients:

$$
\begin{aligned}
w_1(\eta + \pi) &= \alpha w_1(\eta) + \beta w_2(\eta) \\\\
w_1^{\prime}(\eta + \pi) &= \alpha w_1^{\prime}(\eta) + \beta w_2^{\prime}(\eta)
\end{aligned}
$$

where \\(\alpha\\) and \\(\beta\\) are constants determined by the specific solution.

To facilitate this analysis, we choose the following initial conditions at \\(\eta = 0\\):

$$
\begin{aligned}
w_1(0) &= 1, \quad &w_2(0) = 0, \\\\
w_1^{\prime}(0) &= 0, \quad &w_2^{\prime}(0) = 1
\end{aligned}
$$

These conditions normalize the solutions so that \\(w_1(\eta)\\) and \\(w_2(\eta)\\) resemble basic functions like cosine and sine, respectively.

After one period \\(\pi\\), the solution \\(w_1\\) takes the values:

$$
\begin{aligned}
w_1(\pi) &= \alpha, \quad &w_1^{\prime}(\pi) = \beta
\end{aligned}
$$

Here, \\(\alpha\\) and \\(\beta\\) represent the values of \\(w_1(\eta)\\) and its derivative at the point \\(\eta = \pi\\).

The evolution of the solutions after a shift by \\(\pi\\) can be analyzed rigorously using the fundamental matrix \\(Y(\eta)\\):

$$
Y(\eta) = \begin{pmatrix} w_1(\eta) & w_2(\eta) \\\\ w_1^{\prime}(\eta) & w_2^{\prime}(\eta) \end{pmatrix}
$$

Because of our chosen initial conditions, \\(Y(0) = I\\) (the identity matrix). After one period \\(\pi\\), the solutions' state is captured entirely by the **Monodromy matrix** \\(M = Y(\pi)\\):

$$
M = \begin{pmatrix} w_1(\pi) & w_2(\pi) \\\\ w_1^{\prime}(\pi) & w_2^{\prime}(\pi) \end{pmatrix}
$$

This matrix relates the solution state vector \\(w(\eta)\\) to its state one period later:

$$
w(\eta + \pi) = M^T w(\eta)
$$

Also, via Floquet's theorem, we know that for a fundamental solution:

$$
w(\eta + \pi) = \sigma w(\eta)
$$

Thus, according to Floquet's theorem, the constant \\(\sigma\\) must be an eigenvalue of the monodromy matrix \\(M^T\\). To find \\(\sigma\\), we solve the characteristic equation:

$$
|M^T - \sigma I| = \text{det} \begin{pmatrix} w_1(\pi) - \sigma & w_1^{\prime}(\pi) \\\\ w_2(\pi) & w_2^{\prime}(\pi) - \sigma \end{pmatrix} = 0
$$

Expanding the determinant:

$$
(w_1(\pi) - \sigma)(w_2^{\prime}(\pi) - \sigma) - w_1^{\prime}(\pi)w_2(\pi) = 0
$$

This equation is quadratic in \\(\sigma\\), and solving it gives the eigenvalues \\(\sigma_1\\) and \\(\sigma_2\\):

$$
\sigma = \frac{(w_1(\pi) + w_2^{\prime}(\pi)) \pm \sqrt{(w_1(\pi) + w_2^{\prime}(\pi))^2 - 4(w_1(\pi)w_2^{\prime}(\pi) - w_1^{\prime}(\pi)w_2(\pi))}}{2}
$$

The solutions \\(\sigma_1\\) and \\(\sigma_2\\) describe how the original solution scales after one period \\(\pi\\).


Also according to Floquet's theorem, Mathieu's equation will have a solution of the form \\(e^{i\beta \eta} \phi(\eta)\\), where:

$$
\sigma = e^{i\beta \pi},
$$

and:

$$
\phi(\eta) = e^{-i\beta \eta} y(\eta).
$$

This relationship arises because the Floquet multiplier \\(\sigma\\) can be expressed as an exponential term, with \\(\beta\\) being the characteristic exponent. Stable bounded solutions demand that \\(\sigma\\) lies on the complex unit circle, meaning \\(\beta\\) must strictly be a real number.

Given this form, the function \\(\phi(\eta)\\) is periodic with period \\(\pi\\), ensuring:

$$
\phi(\eta + \pi) = e^{-i\beta (\eta + \pi)} y(\eta + \pi) = e^{-i\beta \eta} y(\eta) = \phi(\eta).
$$

This confirms that the solutions exhibit the quasi-periodic behavior predicted by Floquet's theorem, with the eigenvalue \\(\sigma\\) playing a central role in describing the solution's periodicity and scaling.

### 2.2. Hill's Method solution

With Floquet's theorem we assume a series solution, due to G. W. Hill,

{{< alert title="Series solution to Mathieu's equation" color="primary" >}}
$$w = e^{i\beta\eta}\phi(\eta) = e^{i\beta\eta}\sum_{r=-\infty}^{\infty} c_{2r}e^{2ri\eta} = \sum_{r=-\infty}^{\infty} c_{2r}e^{i(\beta+2r)\eta}     $$
(essentially a Fourier expansion, where we have the 2 multiplier since the original function is periodic in \\(\pi\\)).
{{< /alert >}}

When we put this into Mathieu's equation,

$$\sum_{r=-\infty}^{\infty} c_{2r}\left(-(\beta + 2r)^2 + a - 2q\left(\frac{e^{2i\eta} + e^{-2i\eta}}{2}\right)\right)e^{i(\beta+2r)\eta} = 0$$

matching terms in power of r, we get the equation

$$-qc_{2r-2} + (a - (\beta + 2r)^2)c_{2r} - qc_{2r+2} = 0     $$

Dividing by the middle term,

$$\frac{q}{(\beta + 2r)^2 - a}c_{2r-2} - c_{2r} + \frac{q}{(\beta + 2r)^2 - a}c_{2r+2} = 0     $$

To simplify our discussion, let's write

$$\gamma_{2r} = \frac{q}{(\beta + 2r)^2 - a}$$

That these coefficients \\(c_i\\) have non-trivial solutions (linear independence) requires the infinite determinant \\(\Delta\\) to vanish for finite \\(r\\):

$$\Delta(\beta) = \begin{vmatrix} 
\ddots & & & \\\\
\gamma_{-2} & 1 & \gamma_{-2} & &\\\\
& \gamma_0 & 1 & \gamma_0 & \\\\
& & \gamma_2 & 1 & \gamma_2  \\\\
& & & & \ddots
\end{vmatrix} = 0     $$

But of course, this is not a simple object to understand and solve. We can approach this problem from a rather clever angle introduced by E. T. Whittaker.

### 2.2b. Whittaker's approach

Consider the function

$$\lambda = \frac{1}{\cos \pi\beta - \cos \pi\sqrt{a}}$$

Like our determinant, \\(\lambda\\) has a simple pole at \\(a = (\beta + 2r)^2\\), so that the function

$$\zeta = \Delta(\beta) - \kappa\lambda$$

has no singularities if \\(\kappa\\) is chosen properly and is bound at \\(\beta \rightarrow \infty\\), where \\(\Delta(\beta) = 1\\) since the \\(\gamma\\) functions all vanish and the diagonal term is all that remains, and \\(\lambda \rightarrow 0\\) since \\(\cosh(x)\\) in the denominator limits to infinity.

$$\varpi = \Delta(\beta) - \kappa\lambda \rightarrow 1 - 0$$

By Liouville's theorem (of complex calculus), since this limits to a constant, it is a constant always, so we have

$$\kappa = (\Delta(\beta) - 1)\lambda^{-1}$$

Next we consider the \\(\beta = 0\\) case and find,

$$
\begin{aligned}
\kappa &= (\Delta(0) - 1)(1 - \cos \pi\sqrt{a}) \\\\
\Rightarrow \frac{\Delta(\beta) - 1}{\lambda} &= (\Delta(0) - 1)(1 - \cos \pi\sqrt{a})
\end{aligned}
$$

Next we suppose that \\(\beta\\) is chosen to satisfy our requirement that the determinant vanish. We thus have

$$
\begin{aligned}
\cos \pi \beta-\cos \pi\sqrt{a} &= (1-\Delta(0))(1-\cos \pi\sqrt{a}) \\\\
\Rightarrow \beta &= \frac{1}{\pi}\cos^{-1}(1 - \Delta(0)(1 - \cos \pi\sqrt{a}))
\end{aligned}
$$

Recall that our stable solutions require \\(\beta \in \mathbb{R}\\). The mathematical boundary where stability switches to instability occurs when the argument sent to \\(\cos^{-1}\\) breaches the domain \\([-1, 1]\\), at which point \\(\beta\\) forces exponential divergence.

But first we must calculate \\(\Delta(0)\\). 
This task has been made exceedingly simple by the work of J. E. Sträng <a id="cite-strang-2005"></a>[[strang-2005]](#ref-strang-2005) who has found an efficient recursion formula.

### 2.3. Sträng's recursion formula for \\(\Delta(0)\\)

First we note that by the symmetry of \\(\Delta(0)\\), we have \\(\gamma_{-n} = \gamma_n\\). While mathematically infinite, one can compute this determinant numerically by truncating it (taking a finite $K \times K$ subset centered across the main diagonal). Evaluating truncated infinite determinants by expanding minors can quickly yield horrific complexity leaps.

Sträng solved this elegantly by recognizing sub-patterns in the diagonal blocks of the Mathieu matrix, decomposing the nested subset matrix $A_i$ and utilizing recursive Laplace expansion relations.

Without reproducing the full lengthy inductive steps (which trace the removal of matrix columns—right, left, up, and down borders—for nested sub-determinants), the result condenses marvelously. 
By defining successive determinants $\Delta_i$, as well as:

$$\alpha_{2i} = \gamma_{2i}\gamma_{2(i-1)}$$ 

and 

$$\beta_{2i} = 1 - \alpha_{2i}$$

Sträng derives the computationally trivial recursive state:

$$\Delta_i = \beta_{2i}\Delta_{i-1} - \alpha_{2i}\beta_{2i}\Delta_{i-2} + \alpha_{2i}\alpha_{2(i-1)}^2\Delta_{i-3}     $$

We can recursively solve for \\(\Delta(0) = \lim_{i\to\infty} \Delta_i\\) to as much accuracy as necessary. We first must "seed" the recursion with the first three \\(\Delta_i\\). This can be done by hand, though we have deferred to the kindness of our computer algebraic program Maple instead.

Maple finds:

```maple
with(linalg):

C:=matrix([[1,e6,0,0,0,0,0],[e4,1,e4,0,0,0,0],[0,e2,1,e2,0,0,0],
[0,0,e0,1,e0,0,0],[0,0,0,e2,1,e2,0],[0,0,0,0,e4,1,e4],[0,0,0,0,0,e6,1]]):

dc:=det(C);

> dc := -2*e2^2*e0*e4^2*e6+e2^2*e4^2-2*e4^2*e2*e0*e6^2+2*e2*e4^2*e6
+e4^2*e6^2+2*e2^2*e0*e4+4*e2*e0*e6*e4-2*e2*e4-2*e6*e4-2*e2*e0+1

A:= matrix([[1,e4,0,0,0],[e2,1,e2,0,0],[0,e0,1,e0,0],
[0,0,e2,1,e2],[0,0,0,e4,1]]):

da:=det(A);

> da := 1-2*e2*e4-2*e2*e0+2*e2^2*e0*e4+e2^2*e4^2

B:=matrix([[1,e2,0],[e0,1,e0],[0,e2,1]]):

db:=det(B);

> db := 1-2*e2*e0
```

Any algebraic program can get these for us, and below we share python code given that Python is more widely available.

Our program seeks to find regions where the bounded stable solutions of Mathieu's equations exist.

By computing \\(\Delta(0)\\), we construct a Boolean stability mask across the target variable ranges. We check the criteria:

$$ |1 - \Delta(0)(1 - \cos \pi\sqrt{a})| \leq 1 $$
*(alternating to $\cosh$ for negative $a$ due to \\(\cos(ix) = \cosh(x)\\))*

When this argument is bound within \\([-1, 1]\\), \\(\beta \in \mathbb{R}\\), granting stability. If it exceeds 1, exponential divergence destroys the trap orbit.

Our code loops through the \\(a\\) and \\(q\\) parameter grid, outputting the stability Boolean. We perform a contour and filled plot on the matrix block and find the elegant avian-like image of the general stability region of Mathieu's equation:


{{< figure src="mathieu_stability_diagram_01.png" caption="Stability diagram for Mathieu's general equation">}} 


For the quadrupole field, the rf linear Paul trap, we have the following compound stability regime: the stable regions are those in which the fundamental $(a_x, q_x)$ stability diagrams intersect with the scaled mapping for the transverse $(a_z = -2a_x, q_z = -2q_x)$ axes:

{{< figure src="mathieu_stability_diagram_rf_gpu.png" caption="Combined stability diagram bounded region; stable physical configurations must exist inside intersection spaces ensuring containment in all 3 spatial constraints.">}} 

To briefly connect this pure formalism back to standard trapped-ion physics terminology: these stable oscillatory orbits decompose neatly into two superposed elements—a very slow harmonic trap frequency oscillation often called the **secular motion**, riding atop a fast, micro-amplitude jitter occurring perfectly at the high radio drive frequency $\Omega$ called the **micromotion**.

## Synthesis

* The stability diagram derived from Mathieu's equation can be mapped to the physics of keeping ions stably confined. 
* The parameter \\(\beta\\), often referred to as the characteristic Mathieu exponent, corresponds physically to the stability of the ion's trajectory in the trap.
  * When \\(\beta\\) is strictly real, the ion oscillates within a bounded region around the center of the trap, representing an orbit comprised of slow harmonic secular motion coupled with fast driving micromotion.
  * However, when \\(\beta\\) becomes complex, the motion becomes unstable, leading to unbounded oscillations and instantaneous escape from the trap.
* The stability diagram thus maps out regions in the parameter space (characterized by the parameters \\(a\\) and \\(q\\)) which we can map back to physical variables to design functional ion traps.
* Importantly, we must find regions where both the \\(r\\) and the \\(z\\) equations of motion are stable, which corresponds to points on the combined Mathieu's stability diagram where there is an intersection of stability regions between them.
* \\(\mu\\)'s magnitude determines frequency of oscillations of the ion orbits 

## Code calculating the stability regions of Mathieu's equation

### Creating the determinant seeds

In my original experiments I used Maple to get the seeds for the determinant, but Python is open-source, free, and more widely used. Here is how
you can get those seeds with python:


{{< alert title="Getting det seeds in python" color="primary" >}}


In the context of solving Mathieu's equation, we use three key matrices to reflect increasingly large sizes of the larger matrix 
in order to bootstrap our numerical calculations:


Matrix C (7x7):

```
C = [
    [1,  e6, 0,  0,  0,  0,  0 ]
    [e4, 1,  e4, 0,  0,  0,  0 ]
    [0,  e2, 1,  e2, 0,  0,  0 ]
    [0,  0,  e0, 1,  e0, 0,  0 ]
    [0,  0,  0,  e2, 1,  e2, 0 ]
    [0,  0,  0,  0,  e4, 1,  e4]
    [0,  0,  0,  0,  0,  e6, 1 ]
]
```

Matrix C is the largest, a 7x7 tridiagonal matrix. It's symmetric about both diagonals, with the main diagonal consisting of all 1's. The off-diagonals contain e0, e2, e4, and e6 in a symmetric pattern.

Matrix A (5x5):

```
A = [
    [1,  e4, 0,  0,  0 ]
    [e2, 1,  e2, 0,  0 ]
    [0,  e0, 1,  e0, 0 ]
    [0,  0,  e2, 1,  e2]
    [0,  0,  0,  e4, 1 ]
]
```

Matrix A is a 5x5 tridiagonal matrix, essentially a smaller version of matrix C. It maintains the same pattern of 1's on the main diagonal and symmetric placement of e0, e2, and e4 on the off-diagonals.

Matrix B (3x3):

```
B = [
    [1,  e2, 0 ]
    [e0, 1,  e0]
    [0,  e2, 1 ]
]
```

Matrix B is the smallest, a 3x3 tridiagonal matrix. It continues the pattern seen in C and A, but only uses e0 and e2.

* det(C) corresponds to d[3]
* det(A) corresponds to d[2]
* det(B) corresponds to d[1]


The matrices are all odd-sized (3x3, 5x5, 7x7) because Mathieu's equation has solutions that are either even or odd functions. The central row and column in these matrices correspond to the constant term in the Fourier series expansion of the solution.


{{< /alert >}}

{{% tabs "sympy-seeds" %}}
{{% tab "Python (SymPy)" %}}
```python
import sympy as sp

def calculate_mathieu_determinants():
    # Define symbolic variables
    e0, e2, e4, e6 = sp.symbols('e0 e2 e4 e6')

    # Define matrices
    C = sp.Matrix([
        [1, e6, 0, 0, 0, 0, 0],
        [e4, 1, e4, 0, 0, 0, 0],
        [0, e2, 1, e2, 0, 0, 0],
        [0, 0, e0, 1, e0, 0, 0],
        [0, 0, 0, e2, 1, e2, 0],
        [0, 0, 0, 0, e4, 1, e4],
        [0, 0, 0, 0, 0, e6, 1]
    ])

    A = sp.Matrix([
        [1, e4, 0, 0, 0],
        [e2, 1, e2, 0, 0],
        [0, e0, 1, e0, 0],
        [0, 0, e2, 1, e2],
        [0, 0, 0, e4, 1]
    ])

    B = sp.Matrix([
        [1, e2, 0],
        [e0, 1, e0],
        [0, e2, 1]
    ])

    # Calculate determinants
    det_C = C.det()
    det_A = A.det()
    det_B = B.det()

    # Simplify the expressions
    det_C = sp.simplify(det_C)
    det_A = sp.simplify(det_A)
    det_B = sp.simplify(det_B)

    return det_C, det_A, det_B

# Calculate the determinants
d3, d2, d1 = calculate_mathieu_determinants()

# Print the results
print("d[3] =", d3)
print("d[2] =", d2)
print("d[1] =", d1)
print("d[0] = 1")  # This is always 1 by definition
```
{{% /tab %}}
{{% tab "Go (Native)" %}}
Go does not have a standard Computer Algebra System like SymPy or GiNaC. However, writing a simple recursive polynomial evaluator is quite elegant, and perfectly capable of calculating these seeds algebraically!

```go
package main

import (
	"fmt"
	"sort"
	"strings"
)

// Term represents the exponents of e0, e2, e4, e6
type Term struct {
	e0, e2, e4, e6 int
}

func (t Term) str() string {
	if t.e0 == 0 && t.e2 == 0 && t.e4 == 0 && t.e6 == 0 { return "" }
	var p []string
	if t.e0 > 0 { if t.e0 == 1 { p = append(p, "e0") } else { p = append(p, fmt.Sprintf("e0^%d", t.e0)) } }
	if t.e2 > 0 { if t.e2 == 1 { p = append(p, "e2") } else { p = append(p, fmt.Sprintf("e2^%d", t.e2)) } }
	if t.e4 > 0 { if t.e4 == 1 { p = append(p, "e4") } else { p = append(p, fmt.Sprintf("e4^%d", t.e4)) } }
	if t.e6 > 0 { if t.e6 == 1 { p = append(p, "e6") } else { p = append(p, fmt.Sprintf("e6^%d", t.e6)) } }
	return strings.Join(p, "*")
}

// Poly maps a term to its integer coefficient
type Poly map[Term]int

func Term1(coef int, t Term) Poly {
	p := make(Poly)
	if coef != 0 { p[t] = coef }
	return p
}

func (p Poly) Add(other Poly) Poly {
	res := make(Poly)
	for t, c := range p { res[t] = c }
	for t, c := range other {
		res[t] += c
		if res[t] == 0 { delete(res, t) }
	}
	return res
}

func (p Poly) Sub(other Poly) Poly {
	res := make(Poly)
	for t, c := range p { res[t] = c }
	for t, c := range other {
		res[t] -= c
		if res[t] == 0 { delete(res, t) }
	}
	return res
}

func (p Poly) Mul(other Poly) Poly {
	res := make(Poly)
	for t1, c1 := range p {
		for t2, c2 := range other {
			t := Term{t1.e0 + t2.e0, t1.e2 + t2.e2, t1.e4 + t2.e4, t1.e6 + t2.e6}
			res[t] += c1 * c2
			if res[t] == 0 { delete(res, t) }
		}
	}
	return res
}

func (p Poly) String() string {
	if len(p) == 0 { return "0" }
	var terms []string
	for t, c := range p {
		ts := t.str()
		if ts == "" {
			terms = append(terms, fmt.Sprintf("%d", c))
		} else if c == 1 {
			terms = append(terms, ts)
		} else if c == -1 {
			terms = append(terms, "-"+ts)
		} else {
			terms = append(terms, fmt.Sprintf("%d*%s", c, ts))
		}
	}
	sort.Strings(terms)
	
	res := terms[0]
	for i := 1; i < len(terms); i++ {
		if strings.HasPrefix(terms[i], "-") {
			res += " - " + terms[i][1:]
		} else {
			res += " + " + terms[i]
		}
	}
	return res
}

func det(m [][]Poly) Poly {
	n := len(m)
	if n == 1 { return m[0][0] }
	if n == 2 { return m[0][0].Mul(m[1][1]).Sub(m[0][1].Mul(m[1][0])) }

	res := make(Poly)
	for col := 0; col < n; col++ {
		if len(m[0][col]) == 0 { continue }
		
		sub := make([][]Poly, n-1)
		for i := 1; i < n; i++ {
			sub[i-1] = make([]Poly, 0, n-1)
			sub[i-1] = append(sub[i-1], m[i][:col]...)
			sub[i-1] = append(sub[i-1], m[i][col+1:]...)
		}

		cofactor := m[0][col].Mul(det(sub))
		if col%2 == 1 {
			res = res.Sub(cofactor)
		} else {
			res = res.Add(cofactor)
		}
	}
	return res
}

func main() {
	one := Term1(1, Term{0, 0, 0, 0})
	zero := Term1(0, Term{0, 0, 0, 0})
	e0 := Term1(1, Term{1, 0, 0, 0})
	e2 := Term1(1, Term{0, 1, 0, 0})
	e4 := Term1(1, Term{0, 0, 1, 0})
	e6 := Term1(1, Term{0, 0, 0, 1})

	B := [][]Poly{
		{one, e2, zero},
		{e0, one, e0},
		{zero, e2, one},
	}
	
	A := [][]Poly{
		{one, e4, zero, zero, zero},
		{e2, one, e2, zero, zero},
		{zero, e0, one, e0, zero},
		{zero, zero, e2, one, e2},
		{zero, zero, zero, e4, one},
	}
	
	C := [][]Poly{
		{one, e6, zero, zero, zero, zero, zero},
		{e4, one, e4, zero, zero, zero, zero},
		{zero, e2, one, e2, zero, zero, zero},
		{zero, zero, e0, one, e0, zero, zero},
		{zero, zero, zero, e2, one, e2, zero},
		{zero, zero, zero, zero, e4, one, e4},
		{zero, zero, zero, zero, zero, e6, one},
	}

	fmt.Println("d[3] =", det(C))
	fmt.Println("d[2] =", det(A))
	fmt.Println("d[1] =", det(B))
	fmt.Println("d[0] = 1")
}
```
{{% /tab %}}
{{% tab "C++ (GiNaC)" %}}
In C++, computing symbolic algebra is historically handled by third-party libraries like [GiNaC](https://www.ginac.de/). 

*Compile with: `g++ seeds.cpp -lginac -lcln`*

```cpp
#include <iostream>
#include <ginac/ginac.h>

using namespace std;
using namespace GiNaC;

int main() {
    symbol e0("e0"), e2("e2"), e4("e4"), e6("e6");

    matrix C = {
        {1, e6, 0, 0, 0, 0, 0},
        {e4, 1, e4, 0, 0, 0, 0},
        {0, e2, 1, e2, 0, 0, 0},
        {0, 0, e0, 1, e0, 0, 0},
        {0, 0, 0, e2, 1, e2, 0},
        {0, 0, 0, 0, e4, 1, e4},
        {0, 0, 0, 0, 0, e6, 1}
    };

    matrix A = {
        {1, e4, 0, 0, 0},
        {e2, 1, e2, 0, 0},
        {0, e0, 1, e0, 0},
        {0, 0, e2, 1, e2},
        {0, 0, 0, e4, 1}
    };

    matrix B = {
        {1, e2, 0},
        {e0, 1, e0},
        {0, e2, 1}
    };

    cout << "d[3] = " << expand(C.determinant()) << endl;
    cout << "d[2] = " << expand(A.determinant()) << endl;
    cout << "d[1] = " << expand(B.determinant()) << endl;
    cout << "d[0] = 1" << endl;

    return 0;
}
```
{{% /tab %}}
{{% /tabs %}}

### Mathieu's Equation Solver

Many thanks to Christian Schneider for spotting typos in the C++ version!

{{% tabs "mathieu-solver" %}}
{{% tab "Python" %}}
```python
import numpy as np
import matplotlib.pyplot as plt

def calculate_stability(q_range, a_range):
    q_len = len(q_range)
    a_len = len(a_range)
    
    # Preallocate a 2D array for the stability mask
    # 1 for stable (bounded), 0 for unstable
    stability_mask = np.zeros((a_len, q_len))
    
    e = np.zeros(250)
    d = np.zeros(101)
    
    for i, a in enumerate(a_range):
        for j, q in enumerate(q_range):
            # Set all components, guarding against division by zero
            m_values = np.arange(0, 249, 2)
            denom = (m_values ** 2) - a
            # Replace 0 denominators with a very small number to avoid warnings/inf
            denom[denom == 0] = 1e-12 
            e[m_values] = q / denom
            
            # The first seed determinants, from Maple worksheet
            d[3] = (-2*e[2]**2*e[0]*e[4]**2*e[6] + e[2]**2*e[4]**2 - 2*e[4]**2*e[2]*e[0]*e[6]**2 
                    + 2*e[2]*e[4]**2*e[6] + e[4]**2*e[6]**2 + 2*e[2]**2*e[0]*e[4] 
                    + 4*e[2]*e[0]*e[6]*e[4] - 2*e[2]*e[4] - 2*e[6]*e[4] - 2*e[2]*e[0] + 1)
            d[2] = 1 - 2*e[2]*e[4] - 2*e[2]*e[0] + 2*e[2]**2*e[0]*e[4] + e[2]**2*e[4]**2
            d[1] = 1 - 2*e[2]*e[0]
            d[0] = 1
            
            # Sträng's iteration method
            for m in range(4, 101):
                alpha = e[2*m] * e[2*(m-1)]
                beta = 1 - alpha
                alpha1 = e[2*(m-1)] * e[2*(m-2)]
                d[m] = beta * d[m-1] - alpha * beta * d[m-2] + alpha * alpha1**2 * d[m-3]
            
            # Boolean stability test
            if a >= 0:
                arg = 1 - d[100] * (1 - np.cos(np.pi * np.sqrt(a)))
            else:
                arg = 1 - d[100] * (1 - np.cosh(np.pi * np.sqrt(abs(a))))
            
            # Stable iff the argument lies within [-1, 1]
            if abs(arg) <= 1:
                stability_mask[i, j] = 1
                
    return stability_mask

q_min, q_max, q_step = -10, 10, 0.02
a_min, a_max, a_step = -5, 10, 0.05

q_range = np.arange(q_min, q_max, q_step)
a_range = np.arange(a_min, a_max, a_step)

stability_mask = calculate_stability(q_range, a_range)

plt.figure(figsize=(10, 8))
plt.imshow(stability_mask, origin="lower", extent=[q_min, q_max, a_min, a_max], aspect="auto", cmap="viridis")
plt.xlabel('q')
plt.ylabel('a')
plt.title("Stability Diagram for Mathieu's Equation")
plt.savefig('mathieu_stability_diagram_01.png')
#plt.show()
```
{{% /tab %}}
{{% tab "Go" %}}
```go
package main

import (
    "fmt"
    "math"
    "os"
)

func main() {
    fp, err := os.Create("mat.dat")
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer fp.Close()

    var m int
    var e [250]float64
    var d [101]float64
    var alpha, beta, alpha1, arg, a, q float64
    var stable int
    const pi = math.Pi

    // Loop over the desired a-q region
    for q = -10.0; q < 10.0; q += 0.02 {
        for a = -5.0; a < 10.0; a += 0.05 {
            // Set all components
            for m = 0; m <= 248; m += 2 {
                denom := float64(m*m) - a
                if math.Abs(denom) < 1e-12 {
                    denom = 1e-12
                }
                e[m] = q / denom
            }

            // The first seed determinants
            d[3] = -2*e[2]*e[2]*e[0]*e[4]*e[4]*e[6] +
                   e[2]*e[2]*e[4]*e[4] -
                   2*e[4]*e[4]*e[2]*e[0]*e[6]*e[6] +
                   2*e[2]*e[4]*e[4]*e[6] +
                   e[4]*e[4]*e[6]*e[6] +
                   2*e[2]*e[2]*e[0]*e[4] +
                   4*e[2]*e[0]*e[6]*e[4] -
                   2*e[2]*e[4] -
                   2*e[6]*e[4] -
                   2*e[2]*e[0] + 1
                   
            d[2] = 1 - 2*e[2]*e[4] -
                   2*e[2]*e[0] +
                   2*e[2]*e[2]*e[0]*e[4] +
                   e[2]*e[2]*e[4]*e[4]
                   
            d[1] = 1 - 2*e[2]*e[0]
            d[0] = 1

            // Strang's iteration method
            for m = 4; m <= 100; m++ {
                alpha = e[2*m] * e[2*(m-1)]
                beta = 1 - alpha
                alpha1 = e[2*(m-1)] * e[2*(m-2)]
                d[m] = beta*d[m-1] - alpha*beta*d[m-2] + alpha*alpha1*alpha1*d[m-3]
            }

            // Boolean stability test
            if a >= 0 {
                arg = 1 - d[100]*(1 - math.Cos(pi*math.Sqrt(a)))
            } else {
                arg = 1 - d[100]*(1 - math.Cosh(pi*math.Sqrt(math.Abs(a))))
            }

            stable = 0
            if math.Abs(arg) <= 1.0 {
                stable = 1
            }

            // Write to file
            fmt.Fprintf(fp, "%f %f %d\n", q, a, stable)
        }
        fmt.Fprintf(fp, "\n")
    }
}
```
{{% /tab %}}
{{% tab "C++" %}}
```cpp
#include <stdio.h>
#include <math.h>

int main() {
    FILE *fp;
    fp = fopen("mat.dat", "w");
    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }

    int m, stable;
    double e[250], d[101], alpha, beta, alpha1, arg, a, q, denom;
    const double pi = 3.14159265358979323846;

    // Loop over the desired a-q region
    for (q = -10.0; q < 10.0; q += 0.02) {
        for (a = -5.0; a < 10.0; a += 0.05) {
            // Set all components
            for (m = 0; m <= 248; m += 2) {
                denom = (m * m) - a;
                if (fabs(denom) < 1e-12) denom = 1e-12;
                e[m] = q / denom;
            }

            // The first seed determinants
            d[3] = -2 * e[2] * e[2] * e[0] * e[4] * e[4] * e[6] 
                   + e[2] * e[2] * e[4] * e[4]
                   - 2 * e[4] * e[4] * e[2] * e[0] * e[6] * e[6] 
                   + 2 * e[2] * e[4] * e[4] * e[6]
                   + e[4] * e[4] * e[6] * e[6] 
                   + 2 * e[2] * e[2] * e[0] * e[4] 
                   + 4 * e[2] * e[0] * e[6] * e[4]
                   - 2 * e[2] * e[4] 
                   - 2 * e[6] * e[4] 
                   - 2 * e[2] * e[0] + 1;

            d[2] = 1 - 2 * e[2] * e[4] 
                   - 2 * e[2] * e[0] 
                   + 2 * e[2] * e[2] * e[0] * e[4] 
                   + e[2] * e[2] * e[4] * e[4];

            d[1] = 1 - 2 * e[2] * e[0];
            d[0] = 1;

            // Strang's iteration method
            for (m = 4; m <= 100; m++) {
                alpha = e[2 * m] * e[2 * (m - 1)];
                beta = 1 - alpha;
                alpha1 = e[2 * (m - 1)] * e[2 * (m - 2)];
                d[m] = beta * d[m - 1] 
                       - alpha * beta * d[m - 2] 
                       + alpha * alpha1 * alpha1 * d[m - 3];
            }

            // Boolean stability test
            if (a >= 0) {
                arg = 1 - d[100] * (1 - cos(pi * sqrt(a)));
            } else {
                arg = 1 - d[100] * (1 - cosh(pi * sqrt(fabs(a))));
            }

            stable = 0;
            if (fabs(arg) <= 1.0) {
                stable = 1;
            }

            // Write to file
            fprintf(fp, "%f %f %d\n", q, a, stable);
        }
        fprintf(fp, "\n"); // Newline between q blocks
    }

    fclose(fp);
    return 0;
}
```
{{% /tab %}}
{{% /tabs %}}



## References

- **[paul-1990]** **<a id="ref-paul-1990"></a>Paul, W. (1990).** *Electromagnetic traps for charged and neutral particles.* Reviews of Modern Physics. [↩](#cite-paul-1990)
- **[thompson-2002]** **<a id="ref-thompson-2002"></a>Thompson, R.I., Harmon, T.J., Ball, M.G. (2002).** *The rotating-saddle trap: a mechanical analogy to RF-electric-quadrupole ion trapping?* Canadian Journal of Physics. [↩](#cite-thompson-2002)
- **[arscott-1964]** **<a id="ref-arscott-1964"></a>Arscott, F. M. (1964).** *Periodic Differential Equations: An Introduction to Mathieu, Lamé, and Allied Functions.* The MacMillan Company, New York. [↩](#cite-arscott-1964)
- **[mclachlan-1947]** **<a id="ref-mclachlan-1947"></a>McLachlan, N. W. (1947).** *Theory and Application of Mathieu Functions.* Oxford at the Clarendon Press. [↩](#cite-mclachlan-1947)
- **[strang-2005]** **<a id="ref-strang-2005"></a>Sträng, J. E. (2005).** *[On the characteristic exponents of Floquet solutions to the Mathieu equation](http://www.citebase.org/cgi-bin/citations?id=oai:arXiv.org:math-ph/0510076).* Acad. Roy. Belg. Bull. Cl. Sci. [↩](#cite-strang-2005)
- **[leibfried-2003]** **<a id="ref-leibfried-2003"></a>Leibfried, D., et al. (2003).** *Quantum dynamics of single trapped ions.* Rev. Mod. Phys. [↩](#cite-leibfried-2003)
- **[boyce-1996]** **<a id="ref-boyce-1996"></a>Boyce, W. E., DiPrima, R. C. (1996).** *Elementary Differential Equations and Boundary Value Problems.* John Wiley & Sons, Inc. [↩](#cite-boyce-1996)
- **[king-1999]** **<a id="ref-king-1999"></a>King, B. E. (1999).** *[Quantum State Engineering and Information Processing with Trapped Ions](http://jilawww.colorado.edu/www/pubs/thesis/king/).* Ph.D. Thesis. [↩](#cite-king-1999)
