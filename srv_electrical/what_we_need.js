/* What we need, step by step: the change list for Paktronic's quote LF42344,
   shown on the "What we need" tab of both views (the SLD and the site view).
   One copy for both: app_srv_electrical.py inlines this file into each page's
   data script for it, so edit it here only.

   From the handover note on RenewaBlox's revised plan for the Paktronic
   board (27 October 2026), verbatim except where RenewaBlox has since
   changed the plan: step 2 and the line on what stays as quoted now have
   three 250 A rack feeders in place of the quote's two 400 A (November
   2026). Otherwise do not reword, add or drop items. One item was taken
   out of scope by decision: never add it back.
   Keep it plain data: it is inlined into a script element, so no closing
   script tag and no HTML comment opener (the app refuses to serve either). */
const WHAT_WE_NEED = {
  title: 'What we need, step by step',
  steps: [
    { lead: 'Remove the mechanical interlock',
      detail: 'Both ACBs normally closed, so engine, site, grid and data centre share one busbar.',
      owner: 'Paktronic' },
    { lead: 'Three 250 A rack feeders, with trip gear',
      detail: 'Three 250 A rack MCCBs in place of the two 400 A, each with an undervoltage-release coil, a motor operator and status contacts.',
      owner: 'Paktronic' },
    { lead: 'Wire the engine-status trip',
      detail: 'Interposing relay fed by a volt-free "breaker closed" contact on the 2G generator breaker. Contact opens, racks trip.',
      owner: 'Paktronic · 2G · Brook & Mayo' },
    { lead: 'Add the controller watchdog',
      detail: 'Watchdog relay in the same trip circuit. If our controller stops, the racks trip.',
      owner: 'Paktronic' },
    { lead: 'Measure the grid boundary',
      detail: 'Split-core CTs on the transformer incomer cables, wired to a Modbus TCP meter. No copper work on the old board.',
      owner: 'Paktronic' },
    { lead: 'Meter the data centre',
      detail: 'MID-approved meter on the data centre feed. Move the multifunction meter to the CHP incomer. All on Modbus TCP.',
      owner: 'Paktronic' },
    { lead: 'Add a marshalling section',
      detail: 'Controller terminals, Ethernet switch, UPS-backed 230 V supply from the grid side, local/remote switch.',
      owner: 'Paktronic' },
    { lead: 'Issue drawings before build',
      detail: 'Single-line diagram, plus a kiosk plan showing door swings and ACB withdrawal.',
      owner: 'Paktronic' },
    { lead: 'Check the parallel case',
      detail: 'Fault-level and discrimination check with grid and engine feeding the busbar together.',
      owner: 'Paktronic' },
    { lead: 'Prove the trip chain',
      detail: 'At FAT and commissioning, open the engine breaker, then stop the heartbeat. Each must drop the racks.',
      owner: 'Paktronic · RenewaBlox witness' },
    { lead: 'Price changes line by line',
      detail: 'Itemise each change against LF42344, and say whether an 800 A MCCB can replace the data centre ACB.',
      owner: 'Paktronic' },
  ],
  unchanged: 'Everything else on LF42344 stays as quoted: enclosure, ACBs, the cooler and CDU MCCBs, surge protection, phase-failure relays, FAT and commissioning.',
  confirmTitle: 'We confirm before ordering',
  confirm: [
    'FiT generation meter sits upstream of the data centre tee.',
    'Agreed import capacity for the site.',
    'Spare volt-free contact on the 2G generator breaker.',
    'Kiosk is deep enough for the back-to-back boards.',
  ],
};
