## 4. Activation of the equation for the ideal rf Paul trap

Now that we have demonstrated the fundamentals of Mathieu's equation, we can apply it more directly to the ideal rf Paul. Here we follow the outline from [8].

### 4.1. Kapitsa's Secular Approximation

We neglect the DC potential $U$ for now and assume the equations of motion are of the form, for the rf Paul Ideal chamber ion trap:

$$\begin{align*}
\ddot{r} + \frac{2e}{m(r_0^2 + 2z_0^2)}(V \cos \omega t)r &= 0 \\\\
\ddot{z} - \frac{4e}{m(r_0^2 + 2z_0^2)}(V \cos \omega t)z &= 0     
\end{align*}$$

Define $d_0 = r_0^2 + 2z_0^2$. Assume that the $r$ and $z$ motion can be partitioned into large-amp slow "secular" motion $r$ and $z$, and small-amp high frequency micromotion $r_\mu$, $z_\mu$ at the frequency of the applied potential $\omega$. Then our equations become

$$\begin{align*}
\ddot{r} + \ddot{r}_\mu &= -\frac{2e}{md_0^2}(V \cos \omega t)(r + r_\mu) \\\\
\ddot{z} + \ddot{z}_\mu &= \frac{4e}{md_0^2}(V \cos \omega t)(z + z_\mu)     
\end{align*}$$

$$(r_\mu \ll r, \ddot{r}_\mu \gg \ddot{r}) \rightarrow r_\mu \approx +\left(\frac{2eV}{md_0^2\omega^2}r \cos \omega t\right),$$
$$(z_\mu \ll z, \ddot{z}_\mu \gg \ddot{z}) \rightarrow z_\mu \approx -\left(\frac{4eV}{md_0^2\omega^2}z \cos \omega t\right) \quad \exists$$

$$\begin{align*}
\ddot{r} &\approx -\left(\left(\frac{4eV}{md_0^2}\cos \omega t\right) - \left(\frac{4e^2V^2}{m^2d_0^4}\cos^2 \omega t\right)\right)r, \\\\
\ddot{z} &\approx \left(\left(\frac{8eV}{md_0^2}\cos \omega t\right) - \left(\frac{16e^2V^2}{m^2d_0^4}\cos^2 \omega t\right)\right)z \quad \exists
\end{align*}$$

$$\begin{align*}
\ddot{r} &\approx \left(\frac{2e^2V^2}{m^2d_0^4\omega^2}\right)r \rightarrow r \approx -\cos\left(\sqrt{\frac{2eV}{md_0^2}}\omega t\right) = \cos \omega_r t \\\\
\ddot{z} &\approx -\left(\frac{8e^2V^2}{m^2d_0^4\omega^2}\right)z \rightarrow z \approx \cos\left(2\sqrt{\frac{2eV}{md_0^2}}\omega t\right) = \cos \omega_z t
\end{align*}$$

Evidently, $\omega_r = \omega_z/2$. We can thus write,

$$\begin{align*}
r_{tot} &\approx -\cos(\omega_z t/2)\left(

1 - \frac{2eV}{md_0^2\omega^2}\cos \omega t\right) \\\\
z_{tot} &\approx \cos(\omega_z t)\left(1 - \frac{4eV}{md_0^2\omega^2}\cos \omega t\right)
\end{align*}$$

The results of these approximations are graphically displayed in Figures 4.1 and 4.2 created with the following C code:

float w=53;
float wz=4;
float r,z;
float t=0.0;
while(t<1000){
r=-cos(wz*t/2)*(1-0.3*cos(w*t));
z=cos(wz*t)*(1-0.6*cos(w*t));
t+=0.01;}

![Figure 4.1: Secular approximation time series](/path/to/figure4.1.png)

![Figure 4.2: Secular approximation orbits](/path/to/figure4.2.png)

### 4.2. A solution with Mathieu's Equation

For a more formal analysis refer to [6]. Starting with the equation,

$$\frac{d^2z}{d\eta^2} + (a_z - 2q_z \cos(2\eta)) z = 0, \quad \eta = \frac{\omega t}{2}, \quad a_z = \frac{-16eU}{md_0^2\omega^2}, \quad q_z = \frac{-8eV}{md_0^2\omega^2}$$

We apply Floquet's theorem and the subsequent corollary to suppose solutions of the form,

$$u_1(\eta) = e^{\mu\eta}\phi_1(\eta), \quad u_2(\eta) = e^{-\mu\eta}\phi_2(\eta)$$

The conditions for stability require that \\( \mu \\) be purely imaginary. It is typical to write $\mu = \alpha + i\beta$, and so we can take a Fourier expansion of the $\phi$, and recalling that the original equation contains $\cos(2\eta)$, we assume a general solution,

$$z(\eta) = A\sum_{n=-\infty}^{\infty} C_{2n}e^{i(2n+\beta)\eta} + B\sum_{n=-\infty}^{\infty} C_{2n}e^{-i(2n+\beta)\eta}$$

$$z(\eta) = A'\sum_{n=-\infty}^{\infty} C_{2n}\cos((2n + \beta)\eta)$$

As before, we can find a useful recursion relation. Define:

$$D_{2n} \equiv \frac{a_z - (2n + \beta)^2}{q_z} \rightarrow D_{2n}C_{2n} - C_{2n-2} - C_{2n+2} = 0$$

When $n = 0$ we have

$$D_0 = \frac{a_z - \beta^2}{q_z} = \frac{C_{-2}}{C_0} + \frac{C_2}{C_0}$$

With this recursion relationship we may solve for $\beta$ with increasing levels of accuracy, for example,

$$\begin{align*}
C_{2n} &= \frac{C_{2n-2}}{D_{2n}} + \frac{C_{2n+2}}{D_{2n}} \\\\
&= \frac{C_{2n-4}}{D_{2n-2}} + \frac{C_{2n}}{D_{2n-2}} \\\\
&\quad + \frac{C_{2n}}{D_{2n+2}} + \frac{C_{2n+4}}{D_{2n+2}}
\end{align*}$$

As a first approximation, we set $C_{\pm4} = 0$ and obtain

$$D_0 = \frac{1}{D_{-2}} + \frac{1}{D_2}$$

$$\frac{a - \beta^2}{q} = q\left(\frac{1}{a - (-2 + \beta)^2} + \frac{1}{a - (2 + \beta)^2}\right)$$

When we assume $4 \gg \beta^2, \beta, a$ we obtain the approximation,

$$\beta = \sqrt{a + \frac{q^2}{2}}$$

If we take $U = 0 \quad \exists a = 0$ then we find we have recovered the approximation of the previous section,

$$\omega_z = 2\sqrt{\frac{2eV}{md_0^2}}\omega$$

From such references as [8] we know that the next approximation is

$$\beta = \sqrt{a_z + q_z^2\left(\frac{1}{2} + \frac{a}{8}\right) + \frac{q^4}{128}} \cdot \frac{1}{\sqrt{1 - q^2\left(\frac{3}{8} + \frac{5a}{16}\right)}}$$

The motion will have frequencies of $(2n + \beta)$, of which the lowest and second to the lowest correspond roughly with the secular approximation secular and micromotion.

We could carry this process on ad infinitum ad nauseum. This is but one method to solve for $\beta$. The other method is the numerical method we used to find the stable points of the iso-\\( \mu \\). A third method is to use the more technical solutions to the Mathieu equation developed by the mathematicians. We will close this report with a brief review of one such solution.

## 5. Technical details

This form of the solution can be found in many references ([4] for example).

We need consider the case in which our bound periodic solution to the Mathieu equation is of integral order (integer $\times\pi$) and fractional order $\nu\pi$ where $\nu$ is real but may be rational or irrational.

### 5.1. Integral order

We write the Mathieu equation as

$$\frac{d^2y}{dz^2} + (a - 2q \cos(2z))y = 0$$

And consider the case when $q = 0$ and write $a = m^2$ and have solutions $\pm \cos mz, \pm \sin mz$.

We then suppose that the case when $q$ is nonzero can be taken into account as a series based on this initial solution. Let

$$a = 1 + \sum_{i=1}^{\infty} \alpha_i q^i     $$

Then we suppose that

$$y = \cos z + \sum_{i=1}^{\infty} q^i c_i(z)     $$

We determine the nature of the $c_i$ functions as follows. Plugging our solution into the Mathieu equation, we get

$$\begin{align*}
y^{\prime}' &= -\cos z + \sum_{i=1}^{\infty} q^i c_i''(z) \\\\
ay &= \cos z + \sum_{i=1}^{\infty} q^i\left(c_i + \alpha_i \cos z + \sum_{k=1}^{i-1} \alpha_i c_{i-k}\right)
\end{align*}$$

Using the identity

$$\begin{align*}
2 \cos(\frac{1}{2}(A + B)) \cos(\frac{1}{2}(A - B)) &= \frac{(e^{1/2(A+B)} + e^{-1/2(A+B)})(e^{1/2(A-B)} + e^{-1/2(A-B)})}{2} \\\\
&= \frac{e^A + e^{-A}}{2} + \frac{e^B + e^{-B}}{2} \\\\
&= \cos A + \cos B
\end{align*}$$

$$-(2q \cos 2z)y = -q(\cos(z) + \cos(3z) - 2 \cos(2z)\sum_{i=1}^{\infty} q^{i+1} c_1$$

Coefficients are matched:

$$\begin{align*}
q^0 \cos z &= \cos z = 0 \\\\
q^1 c_1'' + c_1 - \cos(3z) + (\alpha_1 - 1) \cos z &= 0 \\\\
q^2 c_2'' + c_2 + \alpha_1 c_1 - 2c_1 \cos 2z + \alpha_2 \cos z &= 0
\end{align*}$$

The particular solution corresponding to $(\alpha_1 - 1) \cos z$ is $\frac{1}{2}(1 - \alpha_1)z \sin z$ which is not bounded, thus we require that $\alpha_1 = 1$ such that

$$c_1'' + c_1 = \cos 3z$$

$$w^{\prime}' + w = A \cos mz \rightarrow w = -\frac{A \cos mz}{(m^2 - 1)} \quad \exists$$

$$c_1 = -\frac{1}{8} \cos 3z$$

The arguments presented before imply that

$$\alpha_2 = -\frac{1}{8} \quad \exists c_2'' + c_2 = \frac{1}{8} \cos 3z - \frac{1}{8} \cos 5z$$

$$\Rightarrow c_2 = -\frac{1}{64} \cos 3z + \frac{1}{192} \cos 5z$$

Following [4], we write

$$\alpha_3 = -\frac{1}{64}, \quad c_3 = -\frac{1}{152}\left(\frac{\cos 3z}{3} - \frac{4 \cos 5z}{9} + \frac{\cos 7z}{18}\right)$$

and so we find the $c$ functions can be represented by "cosine-elliptic" function,

$$\begin{align*}
ce_1(z, q) &= \cos z - \frac{1}{8} q \cos 3z + \frac{1}{64} q^2\left(-\cos 3z + \frac{\cos 5z}{3}\right) \\\\
&\quad -\frac{q^3}{512}\left(\frac{\cos 3z}{3} - \frac{4 \cos 5z}{9} + \frac{\cos 7z}{18}\right) + O(q^4)     
\end{align*}$$

$$a = 1 + q - \frac{q^2}{8} - \frac{q^3}{64} + O(q^4)     $$

### 5.2. Fractional order

Now we suppose solutions of the form

$$ce_\nu(z, q) = \cos \nu z + \sum_{r=1}^{\infty} q^r c_r(z)     $$

$$a = \nu^2 + \sum_{r=1}^{\infty} \alpha_r q^r     $$

Quoting again our references [4, 3], the above procedure may be applied to find,

$$\begin{align*}
ce_\nu(z, q) &= \cos \nu z - \frac{q}{4}\left(\frac{\cos(\nu + 2)z}{\nu + 1} - \frac{\cos(\nu - 2)z}{\nu - 1}\right) \\\\
&\quad + \frac{q^2}{32}\left(\frac{\cos(\nu + 4)z}{(\nu + 1)(\nu + 2)} + \frac{\cos(\nu - 4)z}{(\nu - 1)(\nu - 2)}\right) + O(q^3)     
\end{align*}$$

$$\begin{align*}
a &= \nu^2 + \frac{q^2}{2(\nu^2 - 1)} + \frac{(5\nu^2 + 7)q^4}{32(\nu^2 - 1)^3(\nu^3 - 4)} \\\\
&\quad + \frac{(9\nu^4 + 58\nu^3 + 29)q^6}{64(\nu^2 - 1)^5(\nu^2 - 4)(\nu^2 - 9)} + \cdots     
\end{align*}$$

The latter can be rewritten,

$$\begin{align*}
\nu^2 &= a - \frac{q^2}{2(\nu^2 - 1)} - \frac{(5\nu^2 + 7)q^4}{32(\nu^2 - 1)^3(\nu^3 - 4)} \\\\
&\quad - \frac{(9\nu^4 + 58\nu^3 + 29)q^6}{64(\nu^2 - 1)^5(\nu^2 - 4)(\nu^2 - 9)} - \cdots     
\end{align*}$$

A first approximation is $\nu^2 = a$. Putting this into the $q^2$ coefficient gives a second approximation,

$$\nu^2 = a - \frac{q^2}{2(a - 1)}$$

And repeating the process gives

$$\nu^2 = a - \frac{a - 1}{2(a - 1)^2 - q^2} q^2 - \frac{5a - 7}{32(a - 1)^3(a - 4)} q^4 + O(q^6)$$

Finally we note that $\nu^2 = (m + \beta)^2$ (the integral and fractional component), we have the approximation

$$\beta \approx \left(a - \frac{a - 1}{2(a - 1)^2 - q^2} q^2 - \frac{5a + 7}{32(a - 1)^3(a - 4)} q^5\right)^{1/2} - m     $$

The cosine functions have sine equivalents which we have not included for the sake of brevity. These formulations are not uncommon in the literature, though for obvious reasons the previous derivations were presented in fuller context as they seem to be the preferred method of dealing with the Mathieu equation. But alas, after presenting so many ways of looking at Mathieu's equation, like Pandora's box, last out is hope.

## 6. Mathieu & Maple, forever

Maple 'help' tells us about a number of Mathieu related functions in her tool box, including:

The Mathieu functions MathieuC(a, q, x) and MathieuS(a, q, x) are solutions of the Mathieu differential equation.

MathieuC and MathieuS are even and odd functions of x, respectively.

MathieuFloquet(a, q, x) is a Floquet solution of Mathieu's equation.
where nu = MathieuExponent(a, q) is the characteristic exponent and P(x) is a Pi periodic function.

We present a few plots to demonstrate the usefulness of these functions below.

![Figure 6.1: On the left, the ion is trapped with secular and micromotion; on the right, unbound orbit, the ion is lost forever.](/path/to/figure6.1.png)

![Figure 6.2: A bound orbit, different formal solution ce, and a few of its components](/path/to/figure6.2.png)

![Figure 6.3: The components of the ce function](/path/to/figure6.3.png)

![Figure 6.4: Fascinating behavior of μ as q is varied, a transition from bound to unbound behavior](/path/to/figure6.4.png)

This report has treated, in some detail, the mathematics behind the ideal rf Paul trap. Of course, the actual realization of the trap differs in many important ways from its ideal, but we may approach these realizations, in their many forms, with a fundamental understanding of their operational basis.

## References

[1] Wolfgang Paul, Electromagnetic traps for charged and neutral particles, (Reviews of Modern Physics, Vol. 62, No. 3, July 1990)

[2] R.I. Thompson, T.J. Harmon, M.G. Ball, The rotating-saddle trap: a mechanical analogy to RF-electric-quadrupole ion trapping?, (Canadian Journal of Physics, Dec 2002; 80,12)

[3] F. M. Arscott, Periodic Differential Equations, An Introduction to Mathieu, Lamé, and Allied Functions, (The MacMillan Company, New York 1964)

[4] N. W. McLachlan, Theory and Application of Mathieu Functions, (Oxford at the Clarendon Press, 1947)

[5] Jan Eric Sträng, On the characteristic exponents of Floquet solutions to the Mathieu equation, (Acad. Roy. Belg. Bull. Cl. Sci, to be published 2006; url = http://www.citebase.org/cgi-bin/citations?id=oai:arXiv.org:math-ph/0510076, 2005

[6] Leibried et al., Quantum dynamics of single trapped ions, (Rev. Mod. Phys., Vol. 75, No. 1, January 2003)

[7] W. E. Boyce, R. C. DiPrima, Elementary Differential Equations and Boundary Value Problems, (John Wiley & Sons, Inc., 1996)

[8] King, Brian E., Ph. D. Thesis: Quantum State Engineering and Information Processing with Trapped Ions, (url: http://jilawww.colorado.edu/www/pubs/thesis/king/)
