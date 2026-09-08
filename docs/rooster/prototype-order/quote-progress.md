# JLCPCB quote progress — September 7, 2026

**No complete assembly quote, reservation, cart checkout, payment or order exists.**
The first source-bound candidate upload has reached JLCPCB's sign-in boundary.
Erik has supplied a USA shipping destination; the postal code is recorded in the
private Rooster task note. The postal-code-specific shipping/tax step has not yet
been reached.

## Main-board quote attempt

- Uploaded `fabrication-candidates/4d8e65d-r1/alec-main/alec-main-gerbers.zip`,
  SHA-256 `abee31e91877f17234b467d81afb02f6149a3f7133e2fabc4cf0385453742ac9`.
- JLCPCB detected **4 layers, 64 × 56 mm**, matching the native source and
  independent CAM check.
- Quote configured for **5 fabricated / 2 assembled**, Economic, top assembly,
  customer part selection. Complete THT eligibility still awaits the BOM step.
- Candidate fabrication options: 1.6 mm, green/white, ENIG 1 µin, 1 oz outer and
  inner copper, plugged vias, 0.2 mm minimum drill option, regular outline
  tolerance and flying-probe test. This is a cost-comparison configuration;
  stackup/via treatment are not released manufacturing decisions. The source
  board.yml says 1 oz without separately specifying inner-layer weight.
- Selecting 0.2 mm vias caused the UI to require TG155 material and the additional
  4-wire Kelvin test. Production-file and component-placement review were selected
  with **automatic confirmation disabled** in both dialogs.
- The page showed **$78.38 fabrication/options only** before component/assembly
  pricing. It also displayed **$27.50 DHL Express (DDP)** to the country-level USA
  destination. These figures are incomplete observations for this one board;
  they are not a landed quote, not postal-code-specific, and must not be summed
  or multiplied to estimate the four-board order.
- Clicking Next redirected to JLCPCB sign-in before BOM/CPL upload or component
  matching. Erik has been asked to sign in directly in the preserved browser
  panel. No credentials were read or entered by the agent.

The other three candidate archives have not been uploaded. After sign-in, resume
main component matching, verify assembly scope/rotations and RTC supply, then
quote the three Standard assembly candidates with their rails/fiducials and
detachment requirements. Preserve each complete quote's quantity interpretation,
included services, exclusions and shipping/tax totals before the spending decision.
