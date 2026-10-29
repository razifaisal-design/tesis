# Priestley & Taylor (1972) — Full Text (Original English)

**Citation:** C. H. B. Priestley and R. J. Taylor (1972), "On the Assessment of Surface Heat Flux and Evaporation Using Large-Scale Parameters", *Monthly Weather Review*, 100(2), 81–92.
DOI: 10.1175/1520-0493(1972)100<0081:OTAOSH>2.3.CO;2

**Original PDF in this repository:** `data/raw/1520-0493_1972_100_0081_otaosh_2_3_co_2.pdf`

**Transcription note:** The PDF has a scanned OCR text layer with degraded equations. The prose below was corrected against the page images; equations (1)–(15) were reconstructed from the printed pages (pp. 83–87) and checked against the surrounding text. Obvious OCR corruptions (e.g. "o~vn", "surf ace", "von KBrmBn") have been corrected silently; uncertain readings are marked in the notes at the end.

---

## On the Assessment of Surface Heat Flux and Evaporation Using Large-Scale Parameters

**C. H. B. PRIESTLEY and R. J. TAYLOR** — Division of Atmospheric Physics, Commonwealth Scientific and Industrial Research Organization, Aspendale, Victoria, Australia

**ABSTRACT**—In an introductory review it is reemphasized that the large-scale parameterization of the surface fluxes of sensible and latent heat is properly expressed in terms of energetic considerations over land while formulas of the bulk aerodynamic type are most suitable over the sea. A general framework is suggested.

Data from a number of saturated land sites and open water sites in the absence of advection suggest a widely applicable formula for the relationship between sensible and latent heat fluxes.

For drying land surfaces, we assume that the evaporation rate is given by the same formula for evaporation multiplied by a factor. This factor is found to remain at unity while an amount of water, varying from one site to another, is evaporated. Following this a linear decrease sets in, reducing the evaporation rate to zero after a further 5 cm of evaporation, the same at several sites examined.

### 1. INTRODUCTION

In recent years, advances in our knowledge of larger scale dynamics have placed new requirements on our understanding of boundary layer problems with a consequent emphasis on the mutual nature of the interplay between these two types of process. Students of the boundary layer need to review their understanding in the context of this interplay and must abandon some of the idealizations they have been wont to make; students of the larger scale processes, in turn, are coming to think about the boundary layer as an inherent part of the problem.

Two sharply contrasting philosophies appear to be emerging and it may be useful to discuss the symptoms and arrest the trend before there is an undesirable hardening of attitudes. The "separatist" approach aims to treat the boundary layer development as a closed or quasi-closed problem and to use the solution so obtained to provide lower boundary conditions for the "free" atmosphere. This way of thinking is a direct continuation of the way the subject has developed historically. By contrast, the "merged" approach takes the view that a well designed, sufficiently detailed model of the atmosphere will generate its own special layers, such as the tropopause and the boundary layer, and that it is undesirable to set up a separate computational system for part of the troposphere to serve as input to the remainder.

Clearly, the most important situations for the larger scale dynamics are the changing ones where the time-dependent and advective terms are significant. These are the very cases when the governing conditions of the boundary layers (geostrophic wind, vertical stability, etc.) are subject to changes determined by the atmosphere above and thus are the ones when the separatist approach is least applicable. We must recognize that there is a danger that boundary layer treatments will be consolidated into frameworks that are inherently ill suited for handling the evolutionary aspects of the problems.

This is not to deny that steady-state, one-dimensional treatments still have an important role to play as an essential preliminary to the solution of the more important and complicated evolutionary problems. Again, the separatist approach may have positive advantage in special conditions; for example, when the top of the boundary layer is well defined, as by a sharp inversion, and when conditions in it, though varying to a degree significant for the larger scales, are doing so as a result of purely internal processes.

With whatever vertical flux (heat, vapor, momentum, angular momentum) we are concerned, there are two main facets to the problem: determination of the surface value of the flux and consideration of its variation with height. In principle, the merged approach might look on the first as a boundary condition and the second as something that the large-scale model itself, given sufficient detail, will provide; but to state the problem thus, at the present stage of knowledge and model formulation, is to state it too simply. Beginning quite close to the surface, the vertical flux will be subject to the process of progressive hand-over up the scale of eddy sizes (Priestley 1967). Of special interest is the stage of transition from the subgrid scale to the grid scale—in modeling terms, transition from a stage where the flux requires parameterization to one in which it presumably does not—and this is likely to be a gradual process. Unless these stages are accurately represented in the model, there is the danger that nature's processes will be seriously distorted.

About a decade ago, one of us (Priestley 1959, chapter 8) attempted a systematic appraisal of how the heat flux, and by implication the evaporation, at the surface would behave in time-dependent situations. It emerged from this discussion that three quite different circumstances need to be distinguished:

1. Heating over the sea with an inversion to confine the depth.
2. Heating over the sea without an inversion.
3. Heating over land.

The dominant controls, and hence the evolutionary pattern, are quite different in the three cases.¹ The implication is clear that differences in controls will require differences in parameterization schemes.

The rate of conduction of heat near the interface between two media is governed by the quantity ρ c κ^(1/2) pertaining to each medium. Here ρ is density, c is specific heat (at constant pressure for air), and κ is the thermal diffusivity, molecular or eddy as appropriate. This combination may conveniently be termed the conductive capacity and its typical values respectively for open water, the atmosphere, and solid ground generally form a strongly descending sequence. Heat provided at the interface tends to be conducted into the two media at rates proportional to their conductive capacities.² However, when the thermal balance between the two media is disturbed, as by advection, the heat subsequently passing from one to the other over any not-too-short time is governed by and proportional to the conductive capacity of the lower ranking medium.

Over the oceans, it is probably not unreasonable to look on the fluxes as occasioned by preexisting differences of temperature and humidity between surface and air. Because of the very large conductive capacity of water and because the radiation penetrates into it, the local value of net radiation does not control the evaporation and heat flux into the air. Over the land, it does. For periods of 24 hr or so, the amount of heat taken up or released by the soil is, generally speaking, not a large component of the surface energy balance. Consequently, the available radiant energy exercises a real and immediate physical constraint on the fluxes of vapor and sensible heat over land.

Large-scale dynamical computations, if they are to be extended beyond about 2 days, require as input the rates of evaporation, E, and sensible heat transfer, H, at the earth's surface. We shall consider the minimum requirements to be the daily rates of these quantities, with a spatial resolution comparable with the main network of other observations; that is, to borrow from the Global Atmospheric Research Program (GARP) specifications, on the order of several hundreds of kilometers.

Over land, as indicated above, the sum, LE + H (where L is the latent heat of evaporation of water), is strongly governed by the net radiation, R, at the earth's surface. It is equally clear that the apportionment of energy between LE and H will be governed by the dryness of the ground and, because of the nature of the relationship between saturated vapor pressure and temperature, by the general level of surface temperature, T₀. Parameterization in terms of the slope of the saturated vapor pressure curve has frequently been suggested [e.g., Priestley (1959), Bryson and Kuhn (1962)]. Full consideration of the surface energy balance, not reproduced here but found in any appropriate reference work, shows that T₀ is itself strongly governed by R and ground dryness. Thus, knowledge of R and of ground dryness constitutes a necessary prerequisite for the estimation of the main space variations in daily LE and H on the scale considered here. This paper might well be described as a first attempt to probe, in a practical way, the extent to which the same two prerequisite parameters might also prove sufficient for the purpose in hand.

There will be no room here for detailed discussion as to how one arrives at the two main parameters, R and ground dryness, and the subsidiary parameter, T₀. Suffice it to emphasize that any valid model must provide them before it can aspire to provide LE and H.

It is probable that the fluxes over land on the space scale considered are determined to first order by the radiation actually falling on the area rather than by advected energy. The radiation received will increase as the square of the gridpoint separation, whereas advective effects will increase more or less linearly because the difference in horizontal fluxes of heat and vapor at the upwind and downwind edges of an area will not continue to increase indefinitely as these edges are moved farther apart. While the argument indicates that the grid-scale effects of advection will generally be minor over land, we would hope eventually to be in a state of knowledge where advected energy values would emerge from the calculations, and allowance could be made for them.

Although we shall be concerned with the problem of estimating the total input of heat and vapor to the atmosphere from a large area, the only observations available as a basis are those from individual sites, subject in some cases to quite apparent small-scale nonuniformity and advection. The steps that have been taken to compensate as far as possible for this are described below, but this essential difference between our starting material and what we hope to derive from it must be kept constantly in mind.

### 2. A GENERAL FRAMEWORK

For investigation of the apportionment between heat flux and evaporation, an appropriate framework is provided by the following consideration.

Swinbank and Dyer (1967) have shown that the profiles of specific humidity, q, and temperature, T, are similar over land. Moreover, both the eddy conductivity, K_H, and the eddy diffusivity, K_w, tend to the neutral value of eddy viscosity, k u_* z, at low levels in the turbulent layer or at small z/|L| (Dyer 1967) within the limits of experimental error. Here, k is von Kármán's constant, u_* the friction velocity, z the height, and L the Monin–Obukhov stability length parameter.³ K_H and K_w are then not merely proportional, but are equal. Accordingly, both q and T satisfy the same one-dimensional diffusion equation

```
∂(q, T)/∂t = ∂/∂z [ K ∂(q, T)/∂z ]                              (1)
```

If the surface, denoted by the suffix zero, is saturated, q₀ takes on the saturation value q_s(T₀). Let T̄ be some constant value, central to the range of variation, and consider the variable

```
ψ = q − q_s(T̄) − (∂q_s/∂T)_{T=T̄} (T − T̄)                       (2)
```

This variable also satisfies eq (1). Provided that the range of variation is not too large, we may approximate by "linearizing" the q_s,T curve, which implies that ψ₀ = 0 for all time. It had been earlier concluded by one of the authors (Priestley 1959) that the solution would then be ψ = 0 for all t and z and thus

```
LE/H = (L/c_p)(∂q_s/∂T)_{T=T̄} = s/γ                            (3)
```

c_p is the specific heat of air at constant pressure, s is defined as ∂q_s/∂T at the appropriate temperature, and γ is c_p/L.

However, this is not the most general solution, for ψ can increase or decrease with height without conflicting with eq (1) provided that

```
K ∂ψ/∂z  is independent of z.                                   (4)
```

This complementary function represents any vertical flow through the system without accumulation, and the solution will not be definitive until some further restrictive condition for ψ is identified. Meanwhile, it is appropriate to examine whether or not eq (3) still represents a principal part of the relationship between H and LE. We shall accordingly analyze our data in terms of the quantity, α, defined by

```
LE/(LE + H) = α s/(s + γ).                                      (5)
```

Here, α will be unity for saturated surfaces only in the special case ψ = 0. Clearly, α is related to the Bowen ratio, β (= H/LE), by the relationship

```
β = [1 − α s/(s + γ)] / [α s/(s + γ)].                          (6)
```

The quantity α may also be useful in analyzing data from unsaturated surfaces; in this case, the only a priori expectation would be that α would have a smaller value than for saturated surfaces; indeed, the ratio of the two alphas could be regarded as an index of aridity.

Penman (1948) gave an equation for the rate of evaporation from a saturated soil surface that can be written in the form

```
LE = [s/(s + γ)](R − G) + [γ/(s + γ)] h(q_s − q)                (7a)
```

where R is the net incoming radiation, G is the heat flux into the ground (so that R − G = LE + H), h is a suitably defined transfer coefficient, and q_s is taken at the temperature of the air. In the absence of advection, eq (7a) allows us to put limits that are not entirely intuitive on the possible daily average rate of evaporation. In the first place, it is unlikely that an inversion will prevail so as to make H negative. If H is not negative, then

```
LE < R − G,        i.e., α < (s + γ)/s.                         (7b)
```

Secondly, it is unlikely that the saturation deficit term in eq (7a) will become negative and thus produce condensation. Absence of condensation requires that

```
LE > [s/(s + γ)](R − G),        i.e., α > 1.                    (7c)
```

The term s/(s + γ) varies from 0.56 at a surface temperature of 10°C to 0.82 at 35°C. This temperature range embraces all the observations treated. When the surface is known to be saturated, the conditions (7b, 7c) can be used as minimum criteria for the absence of advective effects.

### 3. EVAPORATION AND HEATING OVER THE LAND (SATURATED SURFACE)

#### a. CSIRO Lysimeters

The Commonwealth Scientific and Industrial Research Organization (CSIRO) lysimeter installation at Aspendale, Victoria, Australia, has been described by McIlroy and Angus (1963). It consists essentially of 12 weighed containers of 1.6-m diameter and 1-m depth. Provision is made for measuring the drainage from each container so that, with due allowance for rainfall, the evaporation can be measured. Only evaporation from pots carrying a pasture crop similar to that on the immediately surrounding area will be considered. The lysimeter pots are irrigated when necessary so that only occasions following heavy rain, when the difference between them and the surrounding countryside is at a minimum, can be used. The records were searched to find days conforming to the following conditions:

1. No rain and no irrigation.
2. At least 0.80 in. of rain in the previous 1, 2, or 3 days (a quite arbitrary definition of "heavy rain").
3. Availability of ancillary data, including 24-hr net radiation, since heat flux is not measured directly at this site, but α can be defined in a form equivalent to eq (5) as

```
α = LE / [ (s/(s + γ))(R − G) ].                                (8)
```

Altogether, 36 days fulfilling these conditions were found and, of those, 14 also satisfied conditions (7b, 7c). Using eq (8), we calculated a mean α of 1.34 ± 0.05 for these 14 days.⁴ Of the 22 days not satisfying conditions (7b, 7c), 21 did not satisfy condition (7b) whereas only one failed to satisfy condition (7c). This would indicate that, in these general weather conditions at least, the site is one where there is convergence of energy by advection so that the value 1.34 for α might be expected to be too high.

In this calculation, 24-hr totals of evaporation and net radiation were used, heat flux into the ground was neglected, and s was calculated at instrument shelter temperature because surface temperatures were not available.

#### b. University of Wisconsin Lysimeter

This installation has been described by Black et al. (1968) and the results of a series of observations with it on a snap bean crop will be presented by Black et al. in a future publication. Copies of the original data on which the latter paper is based have kindly been made available to us. They include evaporation, rainfall, net radiation, surface temperature, and vapor pressure at 1.4-m height for a period of 54 days in July–September 1968. On 23 of these days, condition (7b) was not fulfilled and these are excluded. Condition (7c) was not satisfied on a number of occasions, but judgment on these must be deferred until the degree of saturation of the surface has been considered later in the paper. The days in question are, therefore, not included here.

These observations permit us to evaluate α not only in the form given in eq (8) but also in the equivalent

```
α = LΔq / [ (s/(s + γ))(LΔq + c_pΔT) ]                          (9)
```

where Δ implies a difference over a given height interval. Equations (9) and (8) are equivalent because K_H and K_w are equal. Values of α in both forms [assuming surface saturation in eq (9)] were calculated and plotted against the cumulative total of evaporation minus precipitation, P, since the beginning of the series. For negative values of ∫(E − P)dt greater than 4 cm of water, the two forms [eq (8) and (9)] agree well and this, then, has been taken as the criterion of surface saturation. There are 23 values of α giving a mean of 1.30 ± 0.03.

#### c. Fluxatron Measurements

An interesting series of observations was obtained in March of 1970 (Dyer and Hicks 1970) during a micrometeorological expedition to Gurley in northern New South Wales. Heavy rain (approx. 1.5 in.) fell during the evening of March 16 and observations on the following day can be taken, with some confidence, as referring to a saturated surface of recently plowed bare soil.

That part of the data relevant here comprises 13 half-hourly averages of R, G, and H (the last by eddy correlation technique) accompanied by soil surface temperature and temperature and humidity at 1.5 m. The evaporation rate can be deduced from the surface energy balance.

Both eq (8) and (9) were used to calculate α and the results are given in figure 1. The good agreement between the two estimates of α from 1030 to 1330 LST confirms that the surface was indeed saturated then. The fall-off in true evaporation rate, and the overestimation of it due to the assumption of a saturated surface, as the surface dries out, are clearly shown. The mean α for the period from 1030 to 1330 LST is 1.08 ± 0.01.

This value of α differs significantly from those above, which are similar to others to be discussed below. The explanation offered is that the occasion was one of cold advection; the soil heat flux was, throughout the day, directed upward.

#### d. Wangara Data

An expedition, code-named "Wangara," was made in the winter of 1967 to the neighborhood of Hay in southern New South Wales mainly to investigate mesoscale momentum transfer, but a number of observations were also made that are relevant here. The site provided an extensive area of very good horizontal uniformity. The observations to be used here comprise net radiation, heat flux into the ground, and dry-bulb temperatures at 1, 2, and 4 m together with deduced values of the shearing stress. All details are given by Clarke et al. (1971). Values of heat flux were calculated in lapse conditions according to the flux-gradient relation suggested by Dyer (1967) and in neutral and inversion conditions by assuming that the transfer coefficients for heat and momentum were equal. Evaporation was then determined by energy balance. Only over one period of 6 days immediately following a fall of 1.5 cm of rain can we be reasonably confident that the surface acted as a saturated one, and this period gives α = 1.33 ± 0.21. The comparatively low precision of the determination is no doubt connected with the fact that the fluxes being measured were very small.

### 4. EVAPORATION AND HEATING OVER THE OCEANS

#### a. Heating Beneath an Inversion

When heating occurs over the sea with a well-defined inversion to limit its effects, the conditions are favorable for the application of the separatist approach. An effective, practical, and, to a large extent, definitive treatment of this problem was proposed by Burke (1945), who specified the heat input at the bottom by the bulk aerodynamic formula

```
H₀ = −c_p ρ C u (T − T₀)                                        (10)
```

with a similar formula for moisture input by evaporation. (T and the wind speed, u, are referred to a convenient near-surface standard level.) He assumed that the heat and vapor so supplied to the air were redistributed so as to preserve an adiabatic lapse rate (dry with constant specific humidity up to condensation level and saturated above). He thereby determined the evolutionary behavior of temperature and humidity and the change in height of the mixed (boundary) layer with time and distance due to entrainment. Any change in height due to dynamical influences would presumably be additive.

Equivalently, in terms of friction velocity u_*,

```
H₀ = −c_p ρ C_* u_* (T − T₀).                                   (11)
```

C and C_* are heat transfer coefficients that depend on the reference height selected for T and u, and, if this height is not low enough, on the stability.

Charnock and Ellison (1967) elaborated on this approach, replacing the assumption of an adiabatic profile by the similarity profile

```
k(T − T₀) = [H/(ρ c_p u_*)] [ f(z/L) − ln(z_T/L) ]              (12)
```

with a similar formula for humidity. Here z_T is the thermal equivalent of the roughness length, L is the Monin–Obukhov stability length parameter, and f is the universal function for unstable conditions that has, in effect, been established by experiment (Dyer 1967) at least up to z/|L| = 3. It is a matter for trial whether this more elaborate treatment gives results sufficiently different from Burke's to justify the increased complexity.

Large-scale application, requiring a relationship between the transfer and large-scale variables, may imply some formal preference for eq (11) over (10). More importantly, our reference level for T and u is either so high that variations of C and C_* with stability must be specified or low enough to avoid this difficulty. In the latter case a sufficiently low level must be included in the numerical model.

Because of the arrangement of terms, it has sometimes passed unnoticed that eq (12) is a specific form of eq (11), giving the explicit dependence of C_* on reference height and stability:

```
C_* = k [ f(z/L) − ln(z_T/L) ]^(−1)                             (13)
```

The introduction of similarity arguments may prove of greater practical importance in the determination of H₀ than in problems of the redistribution of heat so gained and of the rise of the top of the heated layer. For these last two problems, Burke's treatment may remain adequate.

#### b. Heating Without an Inversion

When there is no inversion (below the tropopause) to confine the heating, the rate of adjustment of T and T₀ is slower so that large heating rates can be sustained over much longer trajectories. For numerical application, the difficult part of the problem is to know how the medium- and large-scale cumuli will redistribute the heat in the vertical and thereby control the evolution of T.

Even in the presence of turbulence and convection, the transfer of heat is limited by the conductive capacities of the two media (sec. 1). One of the authors (Priestley 1959) was able to obtain interesting evolutionary results and contrasts showing that the sustained heating was not only far greater over water than over land or ice, but that its pattern of time or trajectory dependence had cyclogenetic implications in the one case and anticyclogenetic in the other. Such results should have first-order verisimilitude, but the model was obviously crude, a constant K being used to avoid the pretence of finer understanding. Apart from the use of a transfer-type expression such as eq (10), it is clear that this is not essentially a boundary layer problem nor one of turbulence in the usual sense, and that we must look to a better knowledge of the dynamics of convection to improve our models.

#### c. Parameterization Needs for Energy Fluxes Over the Sea

In either of the two foregoing cases, the heat transfer at the bottom will be given by a formula such as eq (10), (11), or (12) so that the large-scale parameters must include sea-surface temperature and wind, temperature and humidity at the lowest layers of the model, and some measure of stability if this lowest level is more than a few meters above the surface. The dependence of C and C_* on stability can be specified in exact terms only for surface layers up to some tens of meters thick; for the deeper layers, say 100–1000 m, reliable data are only now beginning to emerge (e.g., Clarke 1970).

In subsection 4a, the remaining large-scale parameter is the depth of the mixed layer. This completes the formulation, assuming that no energy (or momentum) penetrates beyond the inversion and that the interaction is purely one of height change, thermally and dynamically produced. The separatist approach, then, has some clear advantages, and Burke (1945) and Charnock and Ellison (1967) have set out the full framework of equations in some detail. In subsection 4b, this advantage disappears because the remaining large-scale parameter is some property of the free atmosphere chosen suitably to indicate its power to transfer heat by convection and because the heating may remain large over sufficient length of trajectory to involve feedback of variability into the large-scale parameters such as u.

### 5. APPLICATION OF ADVECTION-FREE OCEANIC DATA

#### a. The Derivation of α

Although the current local value of net radiation over the sea need not dominate the total exchange, one would expect the ratio LE/H, and hence α as defined by eq (5), in advection-free situations to be determined by processes similar to those discussed in sections 2 and 3. We shall accordingly analyze several sets of high-quality temperature and humidity measurements over water, not only as being relevant to the advection-free value of the ratio over water, but also as adding weight to the determination of this ratio over any saturated surface. The known equality of K_H and K_w over land may be tentatively extended to water surfaces and α may again be expressed by eq (9).

#### b. Indian Ocean Data (CSIRO)

Deacon and Stevenson (1968) have reported observations made on two Indian Ocean cruises numbered Dm 1/62 and G 4/62 of 30 and 27 days, respectively. Use will be made here only of the surface temperatures and temperatures and humidities at 3 m in the air. The average surface temperature and the average air–sea temperature and humidity differences were calculated for each day, and each such average was treated as one observation in what follows. Values of α from these data are, according to eq (9),

1.26 ± 0.01 for Dm 1/62

and

1.30 ± 0.01 for G 4/62.

A number of days showed temperature inversions. Comparatively common, too, were days of very large lapse rates with temperature differences (air–sea) as great as −6°C. These facts suggest that certain days must have been affected by the advection of energy and, in the hope of minimizing such effects, "selected days" (defined as those with a temperature difference, in the lapse sense, lying between 0° and 1°C) were analyzed separately. The resulting values of α are

1.25 ± 0.01 for Dm 1/62 (19 days)

and

1.31 ± 0.01 for G 4/62 (15 days).

Thus, there is no difference on either cruise between the totality of days and those specially selected. This would suggest that the observations are about equally affected by advection of energy toward and away from the areas concerned.

#### c. Indian Ocean (University of Washington)

Paulson (1967) described observations made on 16 days of cruising on the Indian Ocean in February–March 1964. From the maps that he gives, it appears that 9 days (February 22–March 2, omitting February 24 when no observations were made) were spent satisfactorily far from land and only these days have been used. The observations comprised temperature and humidity at six heights (that were not always the same) ranging from 1.14 to 8.15 m. Each day's observations were averaged separately; the resulting average values of c_pT were plotted against those of Lq, and a line was fitted by eye to find the best value of c_pΔT/LΔq. In every case, the points did fit a straight line very closely (as required by the equality of K_H and K_w). Surface temperatures being unavailable, s was found for the air temperature at the lowest level of measurement. The resulting mean value of α is 1.20 ± 0.03.

#### d. Lake Eucumbene

We also include in this section the results of one set of experiments on a large water storage. Webb (1960) in a study of evaporation from Lake Eucumbene gives, among other things, water surface temperature and temperature and humidity at a height of 4 m. The data are given as averages over 3 hr, and for each such period Webb has also given, from his records of wind speed and direction, a statement of the adequacy of the over-water fetch. Only the best cases (fetch of 1 mi or more) have been used and, so as not to limit unnecessarily the number of days available for analysis, only the three 3-hr periods from 0900 to 1800 LST have been taken into account. As will be noted later, 1 mi of fetch over water may be inadequate for an equilibrium state to be set up; nevertheless, the mean α obtained from the 26 available days was 1.25 ± 0.03.

#### e. Atlantic Ocean

When this paper was in an advanced state of preparation, the observations of Hoeber (1970a) came to our attention. These are values of H and LE derived from gradient measurements (making due allowance for thermal stratification) taken over a period of some 2½ weeks in the Atlantic Ocean at the Equator near longitude 30° W. We have used the data as presented in his figure 5 that show the mean diurnal course of these quantities and have calculated the mean values of H and LE. The mean water temperature at 20-cm depth is 25.6°C (Hoeber 1970b) and s has been evaluated at this temperature; the value of α so obtained is 1.30 ± 0.02. Although this value was not originally included in the calculation of the mean α in section 6, it does not in fact disturb it.⁵

### 6. THE VALUE OF α

There is some evidence of warm advection having affected the lysimeter results and cold advection the fluxatron measurements so it seems that the best estimate of α is the overall mean (land and water) of 1.26. This remains the same if the Lake Eucumbene observations are rejected. If the fluxatron results are rejected as being too discordant with the others, the mean is 1.28. This uncertainty in α is hardly important compared with the natural variability of the components E and H. In the following discussion, the evaporation from a horizontally uniform saturated surface (i.e., the potential evaporation, PE) will be given, in energy units, by

```
PE = 1.26 [s/(s + γ)] (R − G).                                  (14)
```

If α is 1.26, it follows from eq (6) that the Bowen ratio

```
β = H/LE = [1 − 1.26 s/(s + γ)] / [1.26 s/(s + γ)]              (15)
```

and is thus a function of the surface temperature. The mean observed value of H/LE from each set of data is compared with that derived from eq (15) in figure 2, indicating that the variation with temperature is correctly accounted for by the inclusion of the factor s/(s + γ) in eq (14). The disparity in the case of the fluxatron observations has already been discussed. The observations were also examined for any possible wind speed dependence. In one case (CSIRO Indian Ocean observations, selected days), there was a statistically significant correlation, but the slope of the regression line was so small that the total variation in α thus predicated was negligible in relation to the general uncertainty in its best value.

In concluding this section, we reiterate that the values of α obtained here are intended primarily for apportioning the net radiation, R, over substantial saturated land areas. They may also be used, with caution, for assigning Bowen ratios (but not apportioning R) in advection-free situations over water. Their inapplicability in the more general context over water is indicated by reference to the climatic atlas of Budyko (1955) where considerable oceanic areas, well removed from land, have monthly heat fluxes directed downward.

### 7. UNSATURATED LAND SURFACES

#### a. Statement of the Problem

When evaporation is to be related to the potential evaporation rate [eq (14)], some measure of soil wetness is obviously needed. This is not to exclude the possibility that other soil and crop parameters may also be necessary. As has been foreshadowed by its use as an independent variable in subsection 3b, the measure chosen is the accumulated actual (not potential) evaporation minus precipitation, as this offers hope of evaluation from the rainfall and radiation records. If the ratio of actual to potential evaporation is a linear function of the accumulated actual evaporation, then it can be shown that this ratio is a negative exponential function of accumulated potential evaporation. This latter relationship is clearly the basis on which the "soil moisture retention tables" of Thornthwaite and Mather (1957) have been calculated.

Data from five different sources have been analyzed to examine the evaporation rate in the drying-out phase.

#### b. CSIRO Lysimeters

Observations from CSIRO lysimeters were found in the records for two periods following heavy rain when no irrigation was applied and good ancillary data existed (although radiation values are absent for some days). They are Feb. 11–25, 1963, and Dec. 2–22, 1968. Other such "drying periods" were also found, but they did not follow heavy rain, and the measurements were clearly much affected by advection; they are not considered here.

In figure 3, these observations are shown as the ratio, actual:potential evaporation rates, plotted against ∫(E − P)dt.

#### c. Three Crops at Katherine, Northern Territory, Australia

Slatyer (1956) reports the results of observations on three crops (cotton, peanuts, and sorghum) at Katherine over 5 weeks of dry weather following heavy rain. The measurements comprise soil moisture [by gypsum block down to 64 in. (1.63 m) with auger sampling down to 8 in. (0.20 m)] and pan evaporation rates. Evaporation from the crops was calculated from the soil moisture and normalized by Slatyer with respect to pan evaporation raised to the power 0.75 (Prescott 1949, 1951).

To make use of these observations, we must assume the following:

1. This system of normalization does, at least approximately, compensate for variations in net radiation, wind speed, etc.
2. The first observation in each crop is at the potential rate—that is, each crop provides a point (not plotted) as (0.0, 1.0) in figure 3.
3. The change in soil moisture adequately measures ∫(E − P)dt.

The results are shown in figure 3.

#### d. Great Plains

Lettau and Davidson (1957) report the results of observations at O'Neill, Nebr., including evaporation rate, net radiation, heat flux into the soil, and soil moisture down to 40 cm (deeper on some days, but a constant depth is needed here). Values of the ordinate in figure 3 can thus be assessed in absolute terms, but the abscissa can only be estimated, relative to an unknown zero, from changes in the water content in the top 40 cm of soil. To locate these observations in figure 3, we drew the line by eye to fit the observations discussed in subsections 7b and 7c and placed the first observation on it. The other points were then positioned in accordance with their location relative to the first observation.

#### e. U.S. Water Conservation Laboratory, Phoenix, Arizona, Lysimeters

Van Bavel (1967) reports a series of observations that are relevant to the present study. A field (5000 m² area) was irrigated by flooding on May 28, 1964, and observations proceeded from May 29 to June 28, at which time the soil water potential had fallen to about −15 bars. The evaporation rate from weighed lysimeters is available together with net radiation and temperature at an unstated height in the air. Soil heat flux was not measured but is stated to be small; in any case, 24-hr totals of evaporation and net radiation are used; therefore, effect of soil heat flux would probably be negligible.

With such a small field, irrigated and in an arid climate, effects of advection must be expected to be considerable and some allowance must be made for them. When the ratio of actual to potential evaporation [the latter from eq (14)] was plotted against time, it stayed reasonably constant until June 17 after which a pronounced downward trend developed. The average value of the ratio during this quasi-constant period was 1.35. Since the general meteorological conditions did not appear to vary greatly, it has been assumed that the effect of advection was to increase all evaporation rates by 35 percent and that they should be divided by 1.35 to approximate those that would have been measured in a horizontally homogeneous situation. The results are shown in figure 4. Comparing figures 3 and 4, we see that a good deal more water was evaporated in the latter case before the evaporation departed from the potential rate, but the equality of the slopes of the descending lines should be noted.

#### f. University of Wisconsin Lysimeters

The data referred to in subsection 3b include a number of days when the surface was clearly not saturated. The results from all observations, excluding only those when LE was greater than R, are shown in figure 5. In this graph, the origin of the abscissa refers to the day when the series of observations started and is thus quite arbitrary in terms of water content because the observations were not begun, as in other cases, immediately after heavy rain or irrigation. The broken line is drawn to have the same slope as the descending lines of figures 3 and 4, and, within the limits imposed by the considerable degree of scatter, the observations can be said to be not inconsistent with it.

#### g. Summary of Drying-Out Results

As the soil dries out, observations over a considerable variety of crops are consistent with the view that the ratio of actual to potential evaporation rate falls off linearly with increasing ∫(E − P)dt and approaches zero when the potential evaporation rate is about 5 cm more than it was when the surface first ceased to behave as a saturated one. The very large degree of scatter in figures 3 and 5 is not really as important as would appear at first sight—the observations have been normalized with respect to radiation and, with the removal of the major cause of variability, the relative effect of others appears magnified.

An important point on which the present analysis can throw no light is knowledge of when evaporation rate first begins to fall below the potential. The CSIRO lysimeter and Katherine crop results would put this point at about ∫(E − P)dt = 4.5 cm so that the soil would be completely dry when 9.5 cm of water had evaporated. [It is interesting to note that Slatyer (1966) has said that the Katherine site, after being thoroughly dried out, can absorb up to about 4 in. (10.2 cm) of rain before runoff begins.] The U.S. Water Conservation Laboratory would put the "downturn" point at about 13 cm and the results from the University of Wisconsin lysimeter indicate that this site can behave as a saturated surface while at least 18 cm of water are evaporated. On the other hand, the bare soil surface of figure 1 shows a decreasing evaporation rate (that was continued on the following days, though not as markedly so as at 1630 LST on Mar. 17, 1970) after only about 0.2 cm of water had evaporated; observers on the spot (Hicks 1970) did, in fact, notice that a visibly dry crust was forming on the soil at this stage.

It is clear that the differences in downturn point evidenced in figures 3, 4, and 5 should be examined with reference to soil, crop, and other factors, but we believe this requires a study in soil–plant water movement for which conclusions should be based on data from a wider distribution of sites than we have been able to assemble.

### 8. CONCLUDING DISCUSSION

In the context of GARP, one of our basic aims must be the specification of heat flux and evaporation over the land surfaces of the globe, and what has been written indicates that an energy approach to the problem is both physically realistic and operationally practical.

However, the apportionment of net radiation between heat flux and evaporation requires a knowledge of the distribution of R itself. This is not the place to discuss how one determines actual or predicted maps of R, but there is a need to make certain general points. The first, and principal, is that the mapping of R (and particularly its predicted value) will be highly sensitive to the knowledge and predictability of cloud amount and type. Here again, then, is not only a feedback process between the boundary layer and the free atmosphere, but also another example of how our prospective ability to link boundary layer considerations into larger scale processes is limited essentially by an ignorance in the latter area; that is, of convection, etc., in this case. Moreover, so severe does this limitation appear to be that it would effectively limit our immediate hopes in the practical mapping of R to the first-order variations in space and time. Hence, the objective has been defined as the mapping of the main variations in the daily totals of R on a space-scale comparable with that of several hundred kilometers already specified for GARP. Although the scales are comparable, they are not identical, for the energy-input mapping must be governed by consideration of the major variations in land form, land use, and hydrology.

In principle, R is calculable from the more elaborate dynamical models, though with what accuracy (bearing in mind particularly its dependence on cloud amount) remains to be seen. R can also be measured directly.⁶ A world network of observations needs to be established:

1. For its own sake.
2. To provide the material for later calculations if these are to eventuate operationally.
3. To encourage every meteorologist to accept net radiation into his daily thinking as one of the basic synoptic variables as would be entirely appropriate in a modernized scientific approach to the subject.

The problem of sampling and representativeness of net radiation is not different in kind from those encountered with the accepted basic elements near the surface (temperature, wind, rainfall, etc.) and the typical accuracy of a good net radiometer, about 5 percent for daily totals, is more than adequate.

Given R, by whatever means, potential evaporation can be estimated from eq (14). It is hoped that other workers will further test the tentative conclusion that α is about 1.26 for saturated surfaces using any good quality advection-free data that has not been treated here. Meanwhile, it seems appropriate to begin to look for possible explanations; that is, what physical considerations might impose the additional constraint on ψ that the analysis of section 2 shows to be involved.

The ratio of molecular diffusivity of water vapor to thermal diffusivity in air has been reviewed by Montgomery (1947) and estimated as about 1.19, more or less independently of temperature (Deacon and Webb 1962). Thus, it does not appear that details of the laminar sublayer can fully explain an α of 1.26, but the possibility that these play some part in the process must not be overlooked.

Some earlier concepts, at least of the lower layers of the marine atmosphere, envisaged these layers as conditioned by the systematic transport of vapor from its source at the surface to a condensation sink in the atmosphere above. This might suggest a mechanism whereby the height, temperature, etc., of the sink exercised control on the general level of q and hence of ψ in the boundary layer. We do not favor this type of explanation, preferring to regard any such sink as an "effect" rather than a "cause."

Moreover, many of the data here were obtained under cloudless conditions; also α > 1 implies a negative ψ (given K_H = K_w) whereas condensation implies a positive ψ in consequence of the curvature of the q_s,T relationship.

It is relevant here to refer to two earlier studies. Linacre (1964) examined the relationship between the temperatures of freely evaporating leaves in bright sunshine and of the air and reached the conclusion that leaves are hotter than the air up to about 33°C and, above that, they are cooler. Priestley (1966) examined this result in terms of the average daily maximum temperature for each month reported by island observing stations and by land stations after periods of heavy rain. His conclusion was that, in the radiation climates that actually exist in nature, air temperatures over a well-watered surface do not rise above 90°–93°F (32°–34°C). Now eq (15) implies that H becomes negative if s/(s + γ) exceeds 1/1.26. This occurs at 32°C (see also fig. 2). The agreement is striking, although its implications may not yet be entirely clear.

Allowances will have to be made for variations in vegetation and soil moisture retention properties when assessing the fluxes from unsaturated surfaces, but this is not entirely a new requirement; knowledge of the vegetation type and amount is implied in the requirement for the estimation of R. Much of the information on water-holding capacity has no doubt already been gathered for agricultural and land-use studies and merely needs to be properly collated to suit it for introduction into meteorology.

It has been made clear that allowance for energy exchange over land in the context of GARP, or in the operational exercises expected to follow from GARP, will require the availability of maps of the appropriate "fixed" boundary conditions; that is, land use and vegetation, albedo (Posey and Clapp 1964), etc. Anticipating the discussion of momentum transfer, a similar need will exist for maps of surface roughness or low-level drag coefficient. Finally, whereas the utilization of the framework discussed here will necessarily involve the prediction of ground moisture, a program of extensive observation will serve not only to improve the technique of prediction but also to provide a continuous updating of initial conditions for the calculations. It is important, therefore, to lend every encouragement to the development of techniques for remote sensing of ground moisture.

### ACKNOWLEDGMENTS

We are grateful to T. A. Black for making available to us the observations discussed in subsections 3b and 6f and to H. Hoeber for supplying the mean water temperature for his Atlantic Ocean observations.

### REFERENCES

Black, T. A., Thurtell, G. W., and Tanner, C. B., "Hydraulic Load Cell Lysimeter, Construction, Calibration, and Tests," *Soil Science Society of America Proceedings*, Vol. 32, No. 5, Madison, Wis., Sept.–Oct. 1968, pp. 623–629.

Bryson, Reid A., and Kuhn, Peter M., "Some Regional Heat Budget Values for Northern Canada," *Geographic Bulletin* No. 17, Geographical Branch, Department of Mines and Technical Surveys, Ottawa, Canada, May 1962, pp. 57–65.

Budyko, M. I. (Editor), "Atlas Teplovago Balansa" (Atlas of Thermal Balance), Glavnaia Geofizcheskaia Observatoriia, Leningrad, U.S.S.R., 1955, 41 pp.

Burke, C. L., "Transformation of Polar Continental Air to Polar Maritime Air," *Journal of Meteorology*, Vol. 2, No. 2, June 1945, pp. 94–112.

Charnock, H., and Ellison, T. H., "The Boundary Layer in Relation to Large-Scale Motions of the Atmosphere and Ocean," *Report of the Study Conference on Global Atmospheric Research Programme (GARP)*, Stockholm, Sweden, June 28–July 11, 1967, ICSU/IUGG Committee on Atmospheric Sciences, COSPAR, World Meteorological Organization, Geneva, Switzerland, Appendix III, 1967, pp. 1–16.

Clarke, R. H., "Observational Studies in the Atmospheric Boundary Layer," *Quarterly Journal of the Royal Meteorological Society*, Vol. 96, No. 407, London, England, Jan. 1970, pp. 91–114.

Clarke, R. H., with Dyer, A. J., Brook, R. R., Reid, D. G., and Troup, A. J., "The Wangara Experiment: Boundary Layer Data," Commonwealth Scientific and Industrial Research Organization, Division of Meteorological Physics, Technical Paper No. 19, Aspendale, Australia, 1971, 352 pp.

Deacon, E. L., and Stevenson, J., "Radiation and Associated Observations Made on Indian Ocean Cruises: Pt. 1. Cruises During 1962," Commonwealth Scientific and Industrial Research Organization, Division of Meteorological Physics, Technical Paper No. 16, Aspendale, Australia, 1968, 22 pp.

Deacon, E. L., and Webb, E. K., "Small-Scale Interactions," *The Sea: Ideas and Observations on Progress in the Study of the Seas: Vol. 1. Physical Oceanography*, Interscience Publishers, New York, N.Y., 1962, 864 pp. (see pp. 43–87).

Dyer, A. J., "The Turbulent Transport of Heat and Water Vapour in an Unstable Atmosphere," *Quarterly Journal of the Royal Meteorological Society*, Vol. 93, No. 398, London, England, Oct. 1967, pp. 501–508.

Dyer, A. J., and Hicks, B. B., "Flux-Gradient Relationships in the Constant Flux Layer," *Quarterly Journal of the Royal Meteorological Society*, Vol. 96, No. 410, London, England, Oct. 1970, pp. 715–721.

Hicks, B. B., CSIRO Division of Atmospheric Physics, Aspendale, Victoria, Australia, 1970 (personal communication).

Hoeber, Heinrich, "Wind-, Temperatur- und Feuchteprofile in der wassernahen Luftschicht über dem äquatorialen Atlantik" (Wind, Temperature and Humidity Profiles in the Surface Air Layer Over the Equatorial Atlantic), "Meteor" Forschungsergebnisse, Reihe B, Heft 3, Gebrüder Borntraeger, Berlin, Germany, 1969, pp. 1–26.

Hoeber, Heinrich, "Measurements in the Atmospheric Surface Layer Above the Tropical Atlantic," *Weather*, Vol. 25, No. 9, London, England, Sept. 1970a, pp. 419–424.

Hoeber, Heinrich, Meteorologisches Institut, Universität Hamburg, Germany, 1970b (personal communication).

Lettau, Heinz H., and Davidson, Ben, "Exploring the Atmosphere's First Mile: Vol. 2. Site Description and Data Tabulation," *Proceedings of the Great Plains Turbulence Field Program, O'Neill, Nebraska, August 1–September 8, 1963*, Pergamon Press, New York, N.Y., 1957, pp. 377–575.

Linacre, E. T., "A note on a Feature of Leaf and Air Temperatures," *Agricultural Meteorology*, Vol. 1, No. 1, Elsevier Publishing Co., Amsterdam, The Netherlands, Mar. 1964, pp. 66–72.

McIlroy, I. C., and Angus, D. E., "The Aspendale Multiple Weighed Lysimeter Installation," Commonwealth Scientific and Industrial Research Organization, Division of Meteorological Physics, Technical Paper No. 14, Aspendale, Australia, 1963, 29 pp.

Montgomery, Ray B., "Viscosity and Thermal Conductivity of Air and Diffusivity of Water Vapour in Air," *Journal of Meteorology*, Vol. 4, No. 6, Dec. 1947, pp. 193–196.

Paulson, Clayton A., "Profiles of Wind Speed, Temperature and Humidity Over the Sea," *Scientific Report*, NSF Grant GP-2418, Department of Atmospheric Sciences, University of Washington, Seattle, Oct. 1967, 128 pp.

Penman, Howard Latimer, "Natural Evaporation From Open Water, Bare Soil and Grass," *Proceedings of the Royal Society of London*, Ser. A, Vol. 193, England, 1948, pp. 120–145.

Posey, Julian W., and Clapp, Philip F., "Global Distribution of Normal Surface Albedo," *Geofisica Internacional*, Vol. 4, No. 1, Mexico City, D. F., Mexico, 1964, pp. 33–48.

Prescott, J. A., "A Climatic Index for the Leaching Factor in Soil Formation," *Journal of Soil Science*, Vol. 1, No. 1, Oxford University Press, London, England, Mar. 1949, pp. 9–19.

Prescott, J. A., "Climatic Expressions and Generalized Climatic Zones in Relation to Soils and Vegetation," *Proceedings of the Specialist Conference in Agriculture: Plant and Animal Nutrition in Relation to Soil and Climatic Factors*, Adelaide and Canberra, Australia, August 22–September 15, 1949, Her Majesty's Stationery Office, London, England, 1951, pp. 27–32.

Priestley, C. H. B., *Turbulent Transfer in the Lower Atmosphere*, The University of Chicago Press, Ill., 1959, 130 pp.

Priestley, C. H. B., "The Limitation of Temperature by Evaporation in Hot Climates," *Agricultural Meteorology*, Vol. 3, No. 3/4, Elsevier Publishing Co., Amsterdam, The Netherlands, 1966, pp. 241–246.

Priestley, C. H. B., "Handover in scale of the fluxes of momentum, heat etc. in the atmospheric boundary layer," *The Physics of Fluids*, Vol. 10, No. 9, Part 2, 1967, pp. S38–S46.

Slatyer, R. O., "Evapotranspiration in Relation to Soil Moisture," *Netherlands Journal of Agricultural Science*, Vol. 4, P. van der Bergh Publishers, Wageningen, The Netherlands, Feb. 1956, pp. 73–76.

Slatyer, R. O., "Agricultural Climatology of the Katherine Area, N.T.," Commonwealth Scientific and Industrial Research Organization, Division of Land Research and Regional Survey, Technical Paper No. 13, Canberra, Australia, Feb. 1966, 39 pp.

Swinbank, W. C., and Dyer, A. J., "An Experimental Study in Micro-Meteorology," *Quarterly Journal of the Royal Meteorological Society*, Vol. 93, No. 398, London, England, Oct. 1967, pp. 494–500.

Thornthwaite, Charles Warren, and Mather, J. R., "Instructions and Tables for Computing Potential Evapotranspiration and the Water Balance," *Publications in Climatology*, Vol. 10, No. 3, Drexel Institute of Technology, Laboratory of Climatology, Philadelphia, Pa., 1957, pp. 185–310.

Van Bavel, C. H. M., "Changes in Canopy Resistance to Water Loss From Alfalfa Induced by Soil Water Depletion," *Agricultural Meteorology*, Vol. 4, No. 3, Elsevier Publishing Co., Amsterdam, The Netherlands, May 1967, pp. 165–176.

Webb, E. K., "An Investigation of the Evaporation From Lake Eucumbene," Commonwealth Scientific and Industrial Research Organization, Division of Meteorological Physics, Technical Paper No. 10, Aspendale, Australia, 1960, 75 pp.

*[Received January 8, 1971; revised June 14, 1971]*

### FIGURE CAPTIONS

**Figure 1.** Fluxatron observations of Mar. 17, 1970; X = LΔq/[(s/(s + γ)) × (LΔq + c_pΔT)] and O = LE/[(s/(s + γ))(R − G)].

**Figure 2.** Ratio of H to LE plotted against temperature. Values for (1) Indian Ocean (University of Washington), (2) Indian Ocean (CSIRO Dm 1/62), (3) Indian Ocean (CSIRO G 4/62), (4) Lake Eucumbene, (5) CSIRO lysimeter, (6) University of Wisconsin lysimeter, (7) fluxatron, (8) Wangara, and (9) Atlantic Ocean are plotted.

**Figure 3.** The drying phase as shown by (X) CSIRO lysimeters, (O) three crops at Katherine, and (Δ) Great Plains.

**Figure 4.** The drying phase as shown by U.S. Water Conservation Laboratory lysimeters.

**Figure 5.** The drying phase as shown by the University of Wisconsin lysimeter. The broken line has been drawn with the same slope as the descending lines of figures 3 and 4.

### FOOTNOTES

1. The case of cooling from below was not included as it was considered less important dynamically though its significance in special processes (e.g., advection fog) is obvious.

2. Note that where eddy-Ks are used or implied, their most appropriate values may depend also on the time scale of the phenomenon: values used in the present time scale (days) would require reconsideration before use in seasonal or climatic-change applications.

3. The use of L in this sense as well as to denote latent heat is standard. No confusion is likely to ensue.

4. This ± notation will be used to denote the standard error of the mean.

5. The standard error was evaluated from mean 24-hr values of H and LE derived from the table given by Hoeber (1969).

6. Whether R is best measured directly on a full network basis or derived from an easier network measurement, such as global radiation by conversion factors obtained from extensive intercomparisons, is a matter for others to discuss; note that such conversion factors will depend on albedo, season, and other variables.

### TRANSCRIPTION NOTES

- The quantity in section 1 read as "ρ c κ^(1/2)" is printed in the OCR layer as "p c , / z"; the reconstruction follows the standard conductive-capacity expression and the surrounding text.
- Equation (12) is printed with "H" (not "H₀") in the numerator; this has been kept as printed.
- Equation (13) is followed in the printed page by the word "exponent.", which appears to be a typesetting artefact; it has been omitted from the equation.
- The Paulson observation heights are printed as "114 to 815 cm" in the OCR; they are rendered here as 1.14 to 8.15 m.
- Lake Eucumbene fetch is printed as "mi"; rendered here as "1 mi".
- Figure captions are reproduced from the printed pages (pp. 84, 87, 88, 89).
