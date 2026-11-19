# Future work and report notes

Written 2026-11-19. Not built into `aerosim/`. Two parts:
- **A.** The honeycomb slice model: the original slides, their errors, the full corrected proof (including the x-direction the slides left blank), and why it is not a backend method.
- **B.** A checklist of what the report should say about the code, with pointers to where the details live.

The tables and bounds in part A are reproduced by `python .agent/checks/slice_model_check.py` (≈ 30 s, asserts included).

---

## A. Honeycomb thermal resistance by slicing

### A.1 The original work

A 10-slide Canva PDF, *Simple Honeycomb Thermal Resistance* (PDF metadata author: Ka Shun Siu). It models a 2-D honeycomb of two materials, walls $k_w$ and cell interiors $k_h$, and builds the in-plane resistance from four ideas:
1. **Slices:** cut perpendicular to the heat flow. Strips in one slice add as parallel conductances, and slices add in series: $R=\int dy/\sum_i k_i x_i(y)$.
2. **Symmetry:** a mirror plane gives two equal halves.
3. **Repeating unit:** an $n\times m$ array scales as $R_{x}=\tfrac nm R_{x,\text{unit}}$ and $R_{y}=\tfrac mn R_{y,\text{unit}}$.
4. **Quarter unit:** two mirror planes cut the unit into quarters. The y-direction is worked on slides 7–9. Slide 10 (x-direction) has five regions drawn and left blank.

**Errors found in the slides (all fixed in A.2):**

| Slide | As written | Fix |
|---|---|---|
| 1 | "No thermal diode" listed as an assumption | Automatic for constant $k$ (linear conduction). The 180° step is proved from geometry (Lemma 3). |
| 1 | Not listed | The real assumption: every slice is at one temperature (A4). It makes the result a **lower bound on R** (A.4). |
| 1 vs 5 | $n$ is both the direction and the column count | Direction renamed $\hat d$ |
| 2 | $L$, $H$ never derived | $L=3l+\sqrt3t$, $H=\sqrt3l+t$ |
| 3 | $R=\int dy/\sum k_ix_i$ | Divide by the depth $l_z$ |
| 4 | Only the parallel combination | The series cut across the mid-plane also needs a reason (it is an isotherm) |
| 8 | Upper limit $\sqrt3(\tfrac56k_w-\tfrac12k_h)t$ | $\sqrt3(\tfrac23k_w-\tfrac16k_h)t$; after ×6, $\sqrt3(4k_w-k_h)t$ (the slide had $5k_w-3k_h$) |
| 8–9 | Divides by $k_w-k_h$ (fails when they are equal) | Log-mean form, valid for any positive $k$ |
| 9 | Denominator $\sqrt3k_hl$ | $3\sqrt3k_hl$ |
| 9 | Expanded log has $3\sqrt3\,k\,t$ | $3\sqrt3\,k_wt$ |
| 10 | x-direction blank | Done in step 6 below |

### A.2 Corrected proof

**Big picture.** Cut the cell into thin slices across the heat flow. Inside a slice the materials sit side by side, so conductances add. Slices stack, so resistances add. Symmetry reduces the job to a quarter of one cell, and scaling takes it back up to the array.

#### 0. Setup
- **A1.** Two homogeneous isotropic materials with constant conductivity: walls $k_w$, cells $k_h$. Perfect contact.
- **A2.** Steady 2-D conduction (nothing varies through the depth $l_z$).
- **A3.** Two opposite faces are isothermal; the other faces are adiabatic.
- **A4 (slice model).** Every thin slice perpendicular to the flow is at one temperature.

With A1 the heat equation is linear, so reversing $\Delta T$ only reverses the flow: $R$ does not depend on direction.

**Sizes.**
- Interior apothem: $\tfrac{\sqrt3}{2}l$. Wall-centreline apothem: $a=\tfrac{\sqrt3}{2}l+\tfrac t2$.
- Centreline side: $s=2a/\sqrt3=l+t/\sqrt3$.
- Vertically stacked cells are $2a$ apart; the nearest cells at the same height are $3s$ apart.

$$H=2a=\sqrt3\,l+t,\qquad L=3s=3l+\sqrt3\,t,\qquad l_x=nL,\quad l_y=mH$$

**Mapping to `aerosim`:** $l=d/\sqrt3$ (d = inner flat-to-flat width) and $H=p=d+t$. The slides' hexagons are flat-top, while `structure/honeycomb.py` `block()` puts cells in rows along x, so they are turned 90°: **the slides' y-direction is the repo's x**.

#### 1. Lemma 1: the slice formula
Take the flow along $y$, and the slice between $y$ and $y+dy$.
- Strip $i$ has width $w_i(y)$, area $l_zw_i$ and length $dy$. By Fourier's law, $dG_i=k_il_zw_i/dy$.
- By A4 every strip sees the same $\Delta T$, so the strips are in parallel: $dG=l_zK(y)/dy$, where $K(y)=\sum_ik_iw_i(y)$.
- The same heat $Q$ crosses every slice, so the slices are in series:

$$R=\frac{1}{l_z}\int_a^b\frac{dy}{K(y)}$$

Below, $\tilde R=l_zR$ (per unit depth). Divide by $l_z$ at the end.

#### 2. Lemmas 2–3: symmetry
- **2a. Mirror plane parallel to the flow.** Geometry and boundary conditions are symmetric, so $T$ is too. Then $\partial T/\partial n=0$ on the plane, so it is adiabatic, and the two halves are in parallel: $R=R_{\text{half}}/2$.
- **2b. Mirror plane perpendicular to the flow, at the midpoint.** The mirror swaps the hot face $T_1$ and the cold face $T_2$. The field $T^*=T_1+T_2-T(\text{mirror}(\mathbf r))$ solves the same problem, so by uniqueness $T^*=T$. On the plane, $T=\tfrac{T_1+T_2}{2}$: it is an isotherm, and the halves are in series, $R=2R_{\text{half}}$.
- **Lemma 3 (180° rotation).** If region B is region A rotated by 180°, then $K_B(y)=K_A(a+b-y)$. The substitution $u=a+b-y$ gives $R_B=R_A$. This is geometry only.

#### 3. Scaling
The unit's edges and centre lines pass through cell centres or wall centres, so they are mirror planes. The unit is four mirrored quarters: two in series and two in parallel, in either direction.

$$\tilde R_{\text{unit}}=2\tilde R_q/2=\tilde R_q,\qquad R_{x,\text{all}}=\frac nmR_{x,\text{unit}},\qquad R_{y,\text{all}}=\frac mnR_{y,\text{unit}}$$

#### 4. Quarter-cell geometry
The origin is at the centre of a horizontal wall, and the quarter is $Q=[0,\tfrac L2]\times[0,\tfrac H2]$. It holds:
- **Hex A**, the interior of the cell centred at $(0,\tfrac H2)$.
- **Hex B**, the interior of the cell centred at $(\tfrac L2,0)$.
- **Wall** everywhere else: half the bottom horizontal wall, the 60° wall, and half the top horizontal wall.

Boundaries:
- **Hex A:** flat bottom $y=\tfrac t2$ for $0\le x\le\tfrac l2$; slanted side $y=\tfrac t2+\sqrt3(x-\tfrac l2)$ from $(\tfrac l2,\tfrac t2)$ to $(l,\tfrac H2)$.
- **Hex B:** leftmost vertex at $x=\tfrac L2-l=\tfrac l2+\tfrac{\sqrt3}{2}t\equiv p$ (the slides' $\tfrac l2+\varepsilon$, with $\varepsilon=\tfrac{\sqrt3}{2}t$ as on slide 8, which is correct); slanted side $y=\sqrt3(x-p)$ for $p\le x\le p+\tfrac l2$; flat top $y=\tfrac{\sqrt3}{2}l$ beyond that.

**Centrosymmetry.** The map $\rho(x,y)=(\tfrac L2-x,\ \tfrac H2-y)$ sends A's centre to B's centre. Hexagons are symmetric under 180° rotation, so $\rho$ swaps A and B and maps wall onto wall. Lemma 3 therefore applies inside the quarter.

#### 5. y-direction
Solving the boundaries for $x$: Hex A's right edge is $x_A(y)=\tfrac l2+\frac{y-t/2}{\sqrt3}$, and Hex B's left edge is $x_B(y)=p+\frac{y}{\sqrt3}$. The regions are $y_1\in[0,\tfrac t2]$, $y_2\in[\tfrac t2,\tfrac{\sqrt3}{2}l]$ and $y_3\in[\tfrac{\sqrt3}{2}l,\tfrac H2]$.

**$y_1$** (no Hex A yet). Using $\tfrac L2-p=l$:
- Cell width: $w_h=\tfrac L2-x_B=l-\tfrac{y}{\sqrt3}$.
- Wall width: $w_w=\tfrac l2+\tfrac{\sqrt3}{2}t+\tfrac{y}{\sqrt3}$.

With $\Delta=k_w-k_h$:

$$K=\frac{\Delta}{\sqrt3}y+D_0,\qquad D_0=\tfrac{\sqrt3}{2}k_wt+\left(\tfrac{k_w}{2}+k_h\right)l$$

$$\tilde R_{y_1}=\frac{\sqrt3}{\Delta}\Big[\ln\!\big(\tfrac{\Delta}{\sqrt3}y+D_0\big)\Big]_0^{t/2}=\frac{\sqrt3}{\Delta}\ln\frac{D_0+\Delta t/(2\sqrt3)}{D_0}$$

At the upper limit the $t$-terms are $\tfrac{\sqrt3}{3}\Delta\tfrac t2+\tfrac{\sqrt3}{2}k_wt=\sqrt3(\tfrac23k_w-\tfrac16k_h)t$. Multiply the top and bottom by 6:

$$E_1=3\sqrt3\,k_wt+(3k_w+6k_h)l,\qquad E_2=E_1+\sqrt3\Delta t=\sqrt3(4k_w-k_h)t+(3k_w+6k_h)l$$

Since $E_2-E_1=\sqrt3\Delta t$, we have $\sqrt3/\Delta=3t/(E_2-E_1)$, so

$$\tilde R_{y_1}=\frac{3t}{\Lambda(E_1,E_2)},\qquad \Lambda(a,b)=\frac{b-a}{\ln(b/a)},\quad \Lambda(a,a)=a$$

$\Lambda$ is the logarithmic mean. Both $E$'s are positive for any positive conductivities, so the result needs no absolute-value bars and no special case when $k_w=k_h$.

**$y_2$.**
- Wall width: $w_w=x_B-x_A=\tfrac{\sqrt3}{2}t+\tfrac{t}{2\sqrt3}=\tfrac{2t}{\sqrt3}$, which is $t/\sin60°$ (a horizontal cut through a 60° wall).
- Cell width: $w_h=\tfrac L2-\tfrac{2t}{\sqrt3}=\tfrac32l-\tfrac{t}{2\sqrt3}$.
- Both are constant over a height of $\tfrac{\sqrt3}{2}l-\tfrac t2$.

Multiply the top and bottom by $2\sqrt3$ (term by term: $3l$, $\sqrt3t$, $4k_wt$, $3\sqrt3k_hl$, $k_ht$):

$$\tilde R_{y_2}=\frac{\frac{\sqrt3}{2}l-\frac t2}{\frac{2}{\sqrt3}k_wt+\frac32k_hl-\frac{k_ht}{2\sqrt3}}=\frac{3l-\sqrt3\,t}{(4k_w-k_h)t+3\sqrt3\,k_hl}$$

**$y_3$.** $\rho$ maps $y_3$ onto $y_1$, so $\tilde R_{y_3}=\tilde R_{y_1}$. Direct check: with $y'=\tfrac H2-y$, $x_A=l-y'/\sqrt3$, which is the same as $w_h$ in $y_1$.

$$\tilde R_{y,q}=2\tilde R_{y_1}+\tilde R_{y_2}$$

#### 6. x-direction (slide 10, completed)
The slices are now vertical strips of width $dx$, with $h_w+h_h=\tfrac H2$, and $\tilde R_x=\int_0^{L/2}dx/K(x)$.

Hex heights from step 4:
- $h_A$ is $\tfrac{\sqrt3}{2}l$ on $[0,\tfrac l2]$, then $\sqrt3(l-x)$ on $[\tfrac l2,l]$, then 0.
- $h_B$ is 0 up to $p$, then $\sqrt3(x-p)$ on $[p,p+\tfrac l2]$, then $\tfrac{\sqrt3}{2}l$.

The breakpoints come in the order $0<\tfrac l2<p\le l<p+\tfrac l2<\tfrac L2$. The middle inequality $p\le l$ is $t\le l/\sqrt3$: **this is where the slides' bound comes from.** Hex A spans $[0,l]$ and Hex B spans $[p,\tfrac L2]$, and every vertical line hits a cell only if these overlap.

| Region | Bounds | Width | $h_h$ | $h_w$ |
|---|---|---|---|---|
| $x_1$ | $0$ to $\tfrac l2$ | $\tfrac l2$ | $\tfrac{\sqrt3}{2}l$ | $\tfrac t2$ |
| $x_2$ | $\tfrac l2$ to $p$ | $\tfrac{\sqrt3}{2}t$ | $\sqrt3(l-x)$ | $\tfrac t2+\sqrt3(x-\tfrac l2)$ |
| $x_3$ | $p$ to $l$ | $\tfrac{l-\sqrt3t}{2}$ | $\tfrac{\sqrt3}{2}l-\tfrac32t$ | $2t$ |
| $x_4$ | $l$ to $p+\tfrac l2$ | $\tfrac{\sqrt3}{2}t$ | $\sqrt3(x-p)$ | $\tfrac H2-\sqrt3(x-p)$ |
| $x_5$ | $p+\tfrac l2$ to $\tfrac L2$ | $\tfrac l2$ | $\tfrac{\sqrt3}{2}l$ | $\tfrac t2$ |

The widths add up to $\tfrac32l+\tfrac{\sqrt3}{2}t=\tfrac L2$. Define

$$D_1=k_wt+\sqrt3\,k_hl,\qquad D_2=(4k_w-3k_h)t+\sqrt3\,k_hl,\qquad D_2-D_1=3\Delta t$$

$D_2$ is positive because $D_2=4k_wt+\sqrt3k_h(l-\sqrt3t)$.

- **$x_1$.** $K=D_1/2$, so $\tilde R_{x_1}=\frac{l/2}{D_1/2}=\frac{l}{D_1}$.
- **$x_2$.** Let $u=x-\tfrac l2\in[0,\tfrac{\sqrt3}{2}t]$. Then $h_h=\tfrac{\sqrt3}{2}l-\sqrt3u$, $h_w=\tfrac t2+\sqrt3u$ and $K=\tfrac{D_1}{2}+\sqrt3\Delta u$:

$$\tilde R_{x_2}=\int_0^{\sqrt3t/2}\frac{du}{\frac{D_1}{2}+\sqrt3\Delta u}=\frac{1}{\sqrt3\Delta}\ln\frac{D_1/2+\frac32\Delta t}{D_1/2}=\frac{1}{\sqrt3\Delta}\ln\frac{D_2}{D_1}=\frac{\sqrt3\,t}{\Lambda(D_1,D_2)}$$

  The last step uses $\frac{1}{\sqrt3\Delta}=\frac{\sqrt3t}{D_2-D_1}$.
- **$x_3$.** Both cells are present: $h_h=\sqrt3(l-x)+\sqrt3(x-p)=\sqrt3(l-p)$, so the slants cancel. $h_w=2t$, which is $t/\cos60°$ (a vertical cut through a 60° wall). $K=2k_wt+k_h(\tfrac{\sqrt3}{2}l-\tfrac32t)=D_2/2$, so $\tilde R_{x_3}=\frac{(l-\sqrt3t)/2}{D_2/2}=\frac{l-\sqrt3t}{D_2}$.
- **$x_4$, $x_5$.** $\rho$ maps $x_5\to x_1$ and $x_4\to x_2$, so $\tilde R_{x_5}=\tilde R_{x_1}$ and $\tilde R_{x_4}=\tilde R_{x_2}$. Direct check of $x_4$ with $v=x-l$: $K=\tfrac{D_2}{2}-\sqrt3\Delta v$, and $\int_0^{\sqrt3t/2}dv/K=\frac{1}{\sqrt3\Delta}\ln\frac{D_2}{D_1}$.

$$\tilde R_{x,q}=2\tilde R_{x_1}+2\tilde R_{x_2}+\tilde R_{x_3}$$

#### 7. Result (valid for $0<t\le l/\sqrt3$)

$$R_{x,\text{all}}=\frac{n}{m\,l_z}\left[\frac{2l}{D_1}+\frac{2\sqrt3\,t}{\Lambda(D_1,D_2)}+\frac{l-\sqrt3\,t}{D_2}\right]$$

$$R_{y,\text{all}}=\frac{m}{n\,l_z}\left[\frac{6t}{\Lambda(E_1,E_2)}+\frac{3l-\sqrt3\,t}{(4k_w-k_h)t+3\sqrt3\,k_hl}\right]$$

The equivalent effective conductivities are $k_x=L/(H\tilde R_{x,q})$ and $k_y=H/(L\tilde R_{y,q})$.

### A.3 Checks
- **Uniform material** ($k_w=k_h=k$). In x, $D_1=D_2=kH$, so $\tilde R_x=\frac{2l+2\sqrt3t+l-\sqrt3t}{kH}=\frac{L}{kH}$. In y, $E_1=E_2=3kL$, so $\tilde R_y=\frac{2t}{kL}+\frac{\sqrt3l-t}{kL}=\frac{H}{kL}$. Both match a plain slab.
- **Closed form vs brute force.** The closed forms agree with a slice integral over a rasterised unit cell to within 0.1% (the script asserts 1%).
- **Against the full 2-D answer.** The repo's own periodic solver (`pixel_fv.solve`, 200 px per $l$) lands between the two bounds in every case. It also matches an independent quarter-cell finite-difference solve (mirror boundary conditions, same resolution; run in the 2026-11-19 session, not kept in the repo) to within 1%.

### A.4 What it costs: the slice model is a bound, not an estimate

**Why it is a bound.** The true temperature field minimises $\int k|\nabla T|^2$ for fixed face temperatures (Dirichlet's principle). A4 restricts the field ($T$ depends on the flow coordinate only), which overestimates the conductance. So $k_{\text{slice}}\ge k_{\text{true}}$, with equality only when $k_w=k_h$.

The dual "lanes" model (strips parallel to the flow with no cross-flow, series inside each lane and lanes in parallel) restricts the heat flux instead. That gives $k_{\text{lane}}\le k_{\text{true}}$ (Thomson's principle). These are the Wiener-type bounds for this geometry.

$R_\text{slice}/R_\text{true}$ (1 means exact):

| $k_w/k_h$ | $t/l$ | x | y |
|---|---|---|---|
| 1 | any | 1.00 | 1.00 |
| 10 | 0.1 | 0.87 | 0.86 |
| 10 | 0.3 | 0.86 | 0.78 |
| 0.1 | 0.1 | 0.72 | 0.72 |
| 0.1 | 0.3 | 0.56 | 0.54 |
| 7692 (4 W/m·K walls, air) | 0.1 | 0.75 | 0.67 |
| 7692 (4 W/m·K walls, air) | 0.3 | 0.78 | 0.65 |

**Why it is off.** A slice cannot see that a wall is tilted. It lets heat go straight through a slanted wall, which is too easy: a wall at angle θ to the flow gets $\cos^2\theta$ of its real resistance. In the thin-wall limit the slice model's solid term tends to $\tfrac23(1-\varphi)k_w$ instead of the $\tfrac12(1-\varphi)k_w$ of `solid/formula.py`.

**At the repo defaults** ($d$ = 30 µm, $t$ = 0.27 µm, $k_w$ = 4 W/m·K, $k_\text{gas}$ = 26.11 mW/m·K, so $t/l$ = 0.0156):

| Method | k⊥ (solid + gas), mW/m·K |
|---|---|
| Lanes (lower bound) | 26.6 |
| Pixel FV (`solid/pixel_fv.py`, PHYSICS.md §7) | 59.2 |
| Formula, φ k_gas + ½(1 − φ) k_wall | 61.2 |
| Slice model, slides' x / y (upper bound) | 78.0 / 74.6 |

**Decision: not a backend method.**
- It is 25–30% high at the FYP geometry: thin walls and a 150:1 contrast are where it is worst.
- In the UI it would show a k⊥ that looks plausible and is wrong, which is what the CLAUDE.md honesty rule is there to stop.
- The bracket from 26.6 to 78 mW/m·K is too wide to be a useful test of Pixel FV. Every lane crosses at least 14.6 of the 15.1 µm half-height in air (the same $t<l/\sqrt3$ condition), so the lower bound is barely above air.

### A.5 Future work
1. **Report section (cheapest, most useful).** Use A.2–A.4 to explain why the thin-wall $\cos^2$ formula is the right fast model and naive series–parallel slicing is not: it is a rigorous upper bound, and 25–30% high here.
2. **Sanity test.** Add `lane ≤ Pixel FV k⊥ ≤ slice` to `.agent/tests/test_detailed.py`. It costs one line on top of `closed_form()` from the check script. It is weak (the bracket is wide), so it is optional.
3. **If the cells are ever filled** (resin in the v1.0 laminate, or a lower contrast): at $k_w/k_h\approx10$ the slice model is within 13–22% on R, so it could then become a fast method labelled "upper bound on k⊥".
4. **Hashin–Shtrikman bounds** (dropped from v0.1 in PLAN.md §0). They hold for any isotropic 2-D two-phase composite, and the honeycomb is isotropic in-plane (see B). At the defaults they give **27.0 ≤ k⊥ ≤ 61.9 mW/m·K**.
   - The upper bound is far tighter than the slice model, and the Formula (61.2) sits about 1% under it.
   - In the thin-wall limit the upper bound $k_w + \varphi/\big(1/(k_h-k_w)+(1-\varphi)/(2k_w)\big)$ with $k_h\to0$ becomes $k_w(1-\varphi)/(1+\varphi)\to\tfrac12(1-\varphi)k_w$. The thin-wall honeycomb reaches the bound, which is a strong defence of `solid/formula.py`.
   - The lower bound is barely above air, like the lanes bound.
   - Adding these is about two lines; the check script already computes them.

---

## B. Report checklist for the code

Things to write in the report, with where the detail already lives. Interim report due **21 Dec 2026**.

**New from this note**
- [ ] **Bounds argument** (A.4, A.5 item 4). Formula (61.2) and Pixel FV (59.2) sit inside the Hashin–Shtrikman bounds, 27.0 ≤ k⊥ ≤ 61.9 mW/m·K, and the Formula is about 1% under the upper one. In the thin-wall limit the honeycomb reaches that bound exactly, so the fast formula is close to the best any isotropic wall/air layout can do. Naive slicing overshoots to 74.6–78.0, which is why the code uses the $\cos^2$ formula.
- [ ] **In-plane isotropy.** A 2-D conductivity tensor unchanged by a 120° rotation is a scalar, so a hexagonal honeycomb has one k⊥ in every in-plane direction. The 5.5% x/y split in Pixel FV (README note 4) is therefore the pixel staircase, not physics, which justifies reporting their mean. The slice model's own x/y split (78.0 vs 74.6) is a model artefact for the same reason.
- [ ] **Extra validation of the solver.** `pixel_fv.solve` reproduces an independent finite-difference solve to within 1% on thick walls at contrasts from 0.1 to 7692 (A.3). This adds to the thin-wall check against the formula.

**Already in the repo docs; the report needs it**
- [ ] **Framework:** k_total = sum of paths, the standard split (Hrubesh & Pekala 1994; Lou 2023). Say that it ignores solid–gas coupling, except Pixel FV, which solves the two together. See PHYSICS.md intro and PLAN.md §2 weakness 1.
- [ ] **Two levels per path**, with the rule that every detailed method reproduces its formula in the ideal case first. See README "Backend" and `.agent/tests/test_detailed.py`.
- [ ] **Input provenance:** status labels measured / literature / derived / hypothetical. k_wall = 4.0 W/m·K is back-calculated from Chan 2022 (PHYSICS.md §2.1). List the hypothetical inputs: ε, κ_w, reflectance, specific extinction e, accommodation α, dT/dx.
- [ ] **Deliberate deviations from the brief:** periodic boundary conditions in Pixel FV (PHYSICS.md §2.2) and the chord-length Monte Carlo gas model (§3.3). Each comes with the test that motivated it.
- [ ] **Shortcuts and limits:**
  - 4-px walls carrying solid fraction s = t/t_draw (§1.2)
  - 2-D ray tracing (§4.3)
  - LBM run on a periodic layer, not the hexagonal pore (§5.2)
  - ν and α in the Rayleigh number fixed at 300 K (§5.1)
- [ ] **Results:**
  - Worked example: 61.3 / 96.8 mW/m·K, anisotropy 1.58.
  - Pixel FV: 59.3 / 95.9, anisotropy 1.62.
  - 5% cracks: k⊥ −23%, anisotropy 2.03 (§7).
- [ ] **Pore-size sweep:** pore size matters through porosity, not size alone (mode C stays flat; §8).
- [ ] **Measured vs model gap:** 16.9 mW/m·K is below the air-only floor of about 26 mW/m·K, so compare trends (§7; PLAN.md §2 weakness 4).
- [ ] **Verification numbers:**
  - Hand numbers matched to 12 digits (`test_hand_numbers.py`)
  - Energy balance ≈ 1e-12
  - 2× grid refinement changes k⊥ by < 3%
  - LBM Nu 2.09 / 2.62 at Ra 5000 / 10 000
- [ ] **Before the interim report (README notes 1–3):**
  - Verify citation page numbers and the Collishaw & Evans DOI.
  - Decide what "pore size" means for gas at low pressure.
  - Present radiation as an order of magnitude until the reflectance spectra are measured.
