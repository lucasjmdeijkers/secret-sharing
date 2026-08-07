# Secret Sharing
This repository implements Shamir's Secret Sharing from scratch, including finite-field arithmetic, polynomial generation, 
and Lagrange interpolation. The implementation avoids third-party cryptographic libraries to expose the underlying mathematics.

## 1. Algorithm

A secret is split into $n$ shares, of which any $t$ shares are sufficient to reconstruct the secret. 
Fewer than $t$ shares provide no information about the secret.

### 1.1 Polynomials
The algorithm exploits the fact that the equation for a polynomial of degree $k$ can be determined <br>
with $k+1$ coordinates. 
<br>
<br>
<img src="images/xplusoneexample.png" width="300">
<br>
<br>
The basic idea is that the secret, when encoded as a number, is the y-intercept of your polynomial.<br>
The degree of the polynomial is your threshold $t-1$. So if $S = 5$ and $t = 3$, we create a polynomial<br>
$y = a_1x^2 + a_2x + 5$ - a quadratic polynomial that requires three points to uniquely define.<br>
The remaining coefficients are sampled randomly, making the polynomial unpredictable without the required number of shares.
It is impossible to know the exact function and thus the secret.<br>

Once the polynomial is built, each shareholder is then given a point on it. 

### 1.2 Finite field
Implementing only the above concept presents two major flaws:<br>
1. <b>Information leak</b><br>If the secret is a large number (i.e. a longer passphrase) the attacker can compare their share value to range the
random noise is sampled from. If the noise is significantly smaller, the secret's magnitude is exposed.<br>


2. <b>Numerical instability</b><br>
When a large amount of shares or shares with relatively high x coordinates are used, the resulting y-coordinate becomes
exponentially large (e.g. moving very far to the right on a parabola). To go from the combined shares to the polynomial
or the directly to the y-intercept via Lagrange interpolation requires division making Python switch to floating-point which, when dealing with numbers that exceed the bit-size representation
(e.g. recurring numbers), can cause precision errors in the less significant digits. This means that the secret can fail
to be reconstructed.

The flaws are addressed by switching to a finite field.. Since the numbers wrap around it is impossible to tell the original magnitudes of the secret and the noise. If the share is 
$10$ it is impossible to know if it is $6+4$ or $6 + 16$ or $30 + 4$, all are equally likely. Additionally, we replace standard
division ($\div a$) with modular inverse ($\times a^{-1} \pmod{p}$), which forces integer-only division.<br>

To do this correctly we have to choose a $p$ which is a) prime and b) bigger than the secret can be (in its decimal form)
, which forces us to restrict the size of the secret. I chose the P-256 field prime which gives a huge search space which
provides security and can contain very large secrets.

## 2. Implementation details
My implementation is simple programming of the logic explained above; but I think two subtle steps deserve explanation.<br>
### 2.1 Secret encoding
Secrets are converted from strings to integers by encoding each character as an 8-bit value and interpreting the resulting 
byte sequence as a big-endian integer. The reverse process is used during reconstruction.

### 2.2 Secret decoding
During reconstruction, the resulting integer is converted back to bytes using repeated division by 2 and remainder extraction, 
then decoded into the original string.


### Relevant materials
#### Wikipedia articles
[Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir's_secret_sharing)<br>
[Endianness](https://en.wikipedia.org/wiki/Endianness)<br>
[Modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic)<br>

#### YouTube videos
[Floating Point Numbers by Computerphile](https://www.youtube.com/watch?v=PZRI1IfStY0)<br>


