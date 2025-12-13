# Secret Sharing
This repository fully recreates the logic and math behind Shamir's Secret Sharing algorithm.<br>
<br>
I attempted to do this as much as possible by hand instead of relying on pre-built solutions<br>
in Python packages authored by others, relying only on a few key built-in packages that come<br>
with Python 3 for unique functionalities which are hard to build myself (e.g. <code>random</code>).

## 1. Algorithm

The algorithm allows a secret ($S$) (e.g. a passphrase, a number) to be split into any number ($n$) <br>
of components ($S_i$), where when a threshold number of shares ($t$) are brought together the secret <br>
is revealed.<br>
<br>
It does not matter which shares are brought together to reach the threshold amount if $t < n$, and <br>
furthermore, no more information is gained about the secret as the number of shares brought <br>
together approaches $t$ (a characteristic called *perfect secrecy*).

### 1.1 Polynomials
The algorithm exploits the fact that the equation for a polynomial of degree $k$ can be determined <br>
with $k+1$ coordinates. For example, a first degree or linear polynomial can be <br>
uniquely defined by two coordinates on the Cartesian plane. For example, the polynomial below passes through <br>
$(1,2)$ and $(2,3)$, from which we can deduce that the polynomial pictured is defined by $y = x+1$. Similarly, <br>
a parabola's equation can be identified if we know three points on the parabola, and so on. 
<br>
<br>
<img src="images/xplusoneexample.png" width="300">
<br>
<br>
The basic idea is that the secret, when encoded as a number, is the y-intercept of your polynomial.<br>
The degree of the polynomial is your threshold $t-1$. So if $S = 5$ and $t = 3$, we create a polynomial<br>
$y = a_1x^2 + a_2x + 5$ - a quadratic polynomial that requires three points to uniquely define.<br>
The coefficients $a_1$ and $a_2$ are randomly chosen and determine the sign and magnitude or the parabola<br>
and the horizontal shift, respectively. This make it so that given less than $t$ shares, it is impossible to know <br>
the exact function and thus the secret.<br>

Once the polynomial is built, each shareholder is than given a point on it. For example, say the resulting<br>
polynomial is $y = x^2 + 2x + 5$ and we want to distribute 4 shares (remember, at least three are needed
so $n \geq t$ must be true). We can give each of the share holders a point in $x \in \{1,2,3,4\}$, so $(1,8)$, $(2,13)$, <br>
$(3,20)$  and $(4,29)$.

### 1.2 Finite field


## 2. Implementation details
My implementation is simple programming of the logic explained above; but I think two subtle steps deserve explanation.<br>
### 2.1 Big Endian conversion 
The secret passed to the main <code>generate_shares</code> function can be any string (e.g. 'dog'). Secret Sharing <br>
involves plotting the secret as the y-intercept on a Cartesian plane, which means it must be converted to a <br>
unique and reversible number. Which is done in function <code>secret_to_decimal</code>. In this script we chose for Big-Endian conversion. <br>
<br>
Once each character of the string is converted to its ASCII value and then its 8-bit binary number,<br>
next the 8-bit binary numbers are concatenated. According to Big Endian order, the order of the letters in the secret
are followed. If the secret is <code>'dog'</code> the string-as-binary value is<code>011001000110111101100111</code>.<br>

Finally, the binary string is interpreted in base-2. Which is done by multiplying each bit by $2$ to the power of its distance from the last bit.
So, $0 \times 2^{23} + 1 \times 2^{22} + 1 \times 2^{21} + 0 \times 2^{20} + \dots + 1 \times 2^1 + 1 \times 2^0$.<br>
Resulting in $6582119$ as the Big Endian representation of <code>'dog'</code>.

### 2.2 Successive division
Of course when decrypting the secret we must be able to go from decimal back to string. Function <code>decimal_to_string</code> 
reverses the above-mentioned conversion process through succesively dividing by two and recording the remainder.
This allows you to rebuild the concatenated binary number.<br>
Next, we simply split the concatenated binary number into its 8-bit parts and we simply convert them back to ASCII and then
to characters, rebuilding the string.


### Sources and further reading
https://en.wikipedia.org/wiki/Shamir's_secret_sharing<br>
https://en.wikipedia.org/wiki/Endianness<br>
https://en.wikipedia.org/wiki/Finite_field_arithmetic<br>
https://en.wikipedia.org/wiki/Modular_arithmetic<br>


