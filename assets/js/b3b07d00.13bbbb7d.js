"use strict";(self.webpackChunkPCB_Design=self.webpackChunkPCB_Design||[]).push([[2561],{6288:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>c,contentTitle:()=>a,default:()=>d,frontMatter:()=>o,metadata:()=>i,toc:()=>l});const i=JSON.parse('{"id":"Scripts/DRC","title":"DRC","description":"3. Design Rule Checking (DRC) Customization","source":"@site/docs/06_Scripts/03_DRC.md","sourceDirName":"06_Scripts","slug":"/Scripts/DRC","permalink":"/STM32-HW-Design-with-KiCAD/docs/Scripts/DRC","draft":false,"unlisted":false,"editUrl":"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/06_Scripts/03_DRC.md","tags":[],"version":"current","sidebarPosition":3,"frontMatter":{},"sidebar":"ScriptSidebar","previous":{"title":"Customized_Footprint","permalink":"/STM32-HW-Design-with-KiCAD/docs/Scripts/Customized_Footprint"},"next":{"title":"Netlist","permalink":"/STM32-HW-Design-with-KiCAD/docs/Scripts/Netlist"}}');var r=t(4848),s=t(8453);const o={},a=void 0,c={},l=[{value:"3. <strong>Design Rule Checking (DRC) Customization</strong>",id:"3-design-rule-checking-drc-customization",level:3},{value:"<strong>Why Customize DRC with Python?</strong>",id:"why-customize-drc-with-python",level:4},{value:"<strong>Common Use Cases for Custom DRC Rules</strong>",id:"common-use-cases-for-custom-drc-rules",level:4},{value:"1. <strong>High-Voltage Clearance Rules</strong>",id:"1-high-voltage-clearance-rules",level:5},{value:"2. <strong>Analog or RF Routing Constraints</strong>",id:"2-analog-or-rf-routing-constraints",level:5},{value:"3. <strong>Thermal Management</strong>",id:"3-thermal-management",level:5},{value:"<strong>Step-by-Step Guide: Implementing a Custom DRC Rule with Python</strong>",id:"step-by-step-guide-implementing-a-custom-drc-rule-with-python",level:4},{value:"<strong>Step 1: Define the Custom Rule</strong>",id:"step-1-define-the-custom-rule",level:5},{value:"<strong>Step 2: Running the Script</strong>",id:"step-2-running-the-script",level:5},{value:"<strong>Step 3: Modifying the Rule</strong>",id:"step-3-modifying-the-rule",level:5},{value:"<strong>Best Practices for Custom DRC Rule Implementation</strong>",id:"best-practices-for-custom-drc-rule-implementation",level:4},{value:"1. <strong>Targeted Rule Application</strong>",id:"1-targeted-rule-application",level:5},{value:"2. <strong>Integration with Existing DRC</strong>",id:"2-integration-with-existing-drc",level:5},{value:"3. <strong>Modular Scripting</strong>",id:"3-modular-scripting",level:5},{value:"4. <strong>Test the Script on Small Sections First</strong>",id:"4-test-the-script-on-small-sections-first",level:5},{value:"5. <strong>Error Reporting</strong>",id:"5-error-reporting",level:5},{value:"<strong>Advanced Custom DRC Example: RF Signal Integrity Check</strong>",id:"advanced-custom-drc-example-rf-signal-integrity-check",level:4},{value:"<strong>Example Custom Rule:</strong>",id:"example-custom-rule",level:5},{value:"<strong>Conclusion</strong>",id:"conclusion",level:4}];function h(e){const n={code:"code",h3:"h3",h4:"h4",h5:"h5",hr:"hr",li:"li",ol:"ol",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,s.R)(),...e.components};return(0,r.jsxs)(r.Fragment,{children:[(0,r.jsxs)(n.h3,{id:"3-design-rule-checking-drc-customization",children:["3. ",(0,r.jsx)(n.strong,{children:"Design Rule Checking (DRC) Customization"})]}),"\n",(0,r.jsx)(n.p,{children:"Design Rule Checking (DRC) is a critical aspect of PCB design, ensuring that the layout adheres to both electrical and manufacturing constraints. While KiCad provides robust built-in DRC rules, there are times when custom design rules are needed for specific projects or when dealing with particular manufacturing requirements. Python scripting in KiCad allows you to extend and customize these DRC checks, enabling you to enforce unique constraints and enhance the reliability of your design."}),"\n",(0,r.jsx)(n.p,{children:"Customizing DRC rules ensures that your design complies not only with standard guidelines but also with any specialized requirements that are essential for the performance, safety, or manufacturability of your PCB. For example, you may need custom rules for high-voltage designs, sensitive analog or RF sections, or complex multi-layer designs."}),"\n",(0,r.jsx)(n.hr,{}),"\n",(0,r.jsx)(n.h4,{id:"why-customize-drc-with-python",children:(0,r.jsx)(n.strong,{children:"Why Customize DRC with Python?"})}),"\n",(0,r.jsx)(n.p,{children:"The default DRC checks in KiCad are comprehensive, but they are designed to cover a broad range of standard design scenarios. In certain projects, especially those involving advanced or specialized PCB designs, you may require more specific rules that go beyond the default checks. Python scripting provides the flexibility to define these additional rules and automate the enforcement of design constraints."}),"\n",(0,r.jsx)(n.p,{children:"Key benefits of using Python for DRC customization:"}),"\n",(0,r.jsxs)(n.ol,{children:["\n",(0,r.jsxs)(n.li,{children:[(0,r.jsx)(n.strong,{children:"Flexibility"}),": You can create custom rules tailored to your project\u2019s unique requirements, whether it's for a specific component, section of the board, or overall design strategy."]}),"\n",(0,r.jsxs)(n.li,{children:[(0,r.jsx)(n.strong,{children:"Automation"}),": Automated rule enforcement saves time and reduces human error, ensuring that critical design checks are not overlooked."]}),"\n",(0,r.jsxs)(n.li,{children:[(0,r.jsx)(n.strong,{children:"Design Assurance"}),": Custom DRC rules ensure that your design will meet not only electrical and physical requirements but also specific safety or reliability guidelines, such as high-voltage isolation or RF interference minimization."]}),"\n"]}),"\n",(0,r.jsx)(n.hr,{}),"\n",(0,r.jsx)(n.h4,{id:"common-use-cases-for-custom-drc-rules",children:(0,r.jsx)(n.strong,{children:"Common Use Cases for Custom DRC Rules"})}),"\n",(0,r.jsxs)(n.h5,{id:"1-high-voltage-clearance-rules",children:["1. ",(0,r.jsx)(n.strong,{children:"High-Voltage Clearance Rules"})]}),"\n",(0,r.jsx)(n.p,{children:"In high-voltage designs, ensuring proper spacing between certain components and traces is critical to prevent arcing or breakdowns. Python can be used to enforce additional clearance rules in specific areas of the board, such as between high-voltage nets and low-voltage components."}),"\n",(0,r.jsx)(n.p,{children:(0,r.jsx)(n.strong,{children:"Example Use Case:"})}),"\n",(0,r.jsxs)(n.ul,{children:["\n",(0,r.jsx)(n.li,{children:"For any traces connected to high-voltage nets, enforce a clearance of 2 mm or more from nearby components, which is essential for safety and to prevent electrical discharge."}),"\n"]}),"\n",(0,r.jsxs)(n.h5,{id:"2-analog-or-rf-routing-constraints",children:["2. ",(0,r.jsx)(n.strong,{children:"Analog or RF Routing Constraints"})]}),"\n",(0,r.jsx)(n.p,{children:"Sensitive analog or RF signals often require specialized routing constraints, such as controlled impedance, isolation from noisy digital signals, or specific trace lengths. A Python script can enforce these constraints by checking the layout for compliance with analog or RF design best practices."}),"\n",(0,r.jsx)(n.p,{children:(0,r.jsx)(n.strong,{children:"Example Use Case:"})}),"\n",(0,r.jsxs)(n.ul,{children:["\n",(0,r.jsx)(n.li,{children:"Ensure that traces in RF sections have proper isolation from digital or power traces, maintaining a predefined minimum clearance."}),"\n",(0,r.jsx)(n.li,{children:"Verify that traces in high-frequency sections follow controlled impedance routing and avoid sharp bends, which could introduce signal integrity issues."}),"\n"]}),"\n",(0,r.jsxs)(n.h5,{id:"3-thermal-management",children:["3. ",(0,r.jsx)(n.strong,{children:"Thermal Management"})]}),"\n",(0,r.jsx)(n.p,{children:"Thermal considerations in PCB design require special handling, especially for components that generate significant heat. Custom DRC rules can ensure that thermal vias are placed properly and that there is adequate spacing for heat dissipation."}),"\n",(0,r.jsx)(n.p,{children:(0,r.jsx)(n.strong,{children:"Example Use Case:"})}),"\n",(0,r.jsxs)(n.ul,{children:["\n",(0,r.jsx)(n.li,{children:"Enforce the placement of thermal vias for components with high power dissipation, ensuring that there is adequate heat sinking to a ground plane or copper pour."}),"\n",(0,r.jsx)(n.li,{children:"Check for sufficient copper thickness on traces carrying high current to prevent overheating."}),"\n"]}),"\n",(0,r.jsx)(n.hr,{}),"\n",(0,r.jsx)(n.h4,{id:"step-by-step-guide-implementing-a-custom-drc-rule-with-python",children:(0,r.jsx)(n.strong,{children:"Step-by-Step Guide: Implementing a Custom DRC Rule with Python"})}),"\n",(0,r.jsx)(n.p,{children:'Let\u2019s walk through an example of how to create a custom DRC rule that enforces additional clearance for high-voltage traces in a design. The goal is to automatically check for a minimum 2 mm clearance between any net classified as "high-voltage" and all other components or traces.'}),"\n",(0,r.jsx)(n.h5,{id:"step-1-define-the-custom-rule",children:(0,r.jsx)(n.strong,{children:"Step 1: Define the Custom Rule"})}),"\n",(0,r.jsx)(n.p,{children:"The first step is to define the custom rule that needs to be enforced. In this case, we\u2019ll create a rule that checks the clearance between high-voltage traces and other parts of the board."}),"\n",(0,r.jsx)(n.pre,{children:(0,r.jsx)(n.code,{className:"language-python",children:'import pcbnew\n\ndef check_high_voltage_clearance(board):\n    # Define the high-voltage nets\n    high_voltage_nets = ["HV_NET1", "HV_NET2"]  # Example high-voltage nets\n\n    # Define the required clearance (in mm)\n    min_clearance = 2.0\n\n    # Get all tracks from the board\n    tracks = board.GetTracks()\n\n    # Loop through each track and check clearance\n    for track in tracks:\n        net_name = track.GetNetname()\n\n        # Check if the track belongs to a high-voltage net\n        if net_name in high_voltage_nets:\n            track_clearance = track.GetClearance()\n\n            # Check clearance from other components and traces\n            for other_track in tracks:\n                if other_track != track:\n                    distance = track.GetDistance(other_track)\n\n                    # If distance is less than required clearance, raise a DRC error\n                    if distance < min_clearance * 1000000:  # KiCad stores distances in nanometers\n                        print(f"DRC Error: High-voltage net {net_name} is too close to another net.")\n                        return False\n\n    print("All high-voltage clearance checks passed.")\n    return True\n\n# Example usage\nboard = pcbnew.GetBoard()\ncheck_high_voltage_clearance(board)\n'})}),"\n",(0,r.jsx)(n.h5,{id:"step-2-running-the-script",children:(0,r.jsx)(n.strong,{children:"Step 2: Running the Script"})}),"\n",(0,r.jsx)(n.p,{children:"Once the script is defined, you can run it directly within KiCad\u2019s Python scripting console. The script will loop through all the traces on the board, check for high-voltage nets, and then verify that they maintain the required 2 mm clearance from other components and traces. If any violations are found, the script will print a DRC error message."}),"\n",(0,r.jsx)(n.h5,{id:"step-3-modifying-the-rule",children:(0,r.jsx)(n.strong,{children:"Step 3: Modifying the Rule"})}),"\n",(0,r.jsx)(n.p,{children:"You can easily modify this script to enforce different types of rules, such as:"}),"\n",(0,r.jsxs)(n.ul,{children:["\n",(0,r.jsx)(n.li,{children:"Varying the clearance requirement for different nets or components."}),"\n",(0,r.jsx)(n.li,{children:"Adding specific checks for particular component types, such as through-hole vs. surface-mount components."}),"\n",(0,r.jsx)(n.li,{children:"Implementing more advanced checks, such as verifying controlled impedance or via placement around sensitive components."}),"\n"]}),"\n",(0,r.jsx)(n.hr,{}),"\n",(0,r.jsx)(n.h4,{id:"best-practices-for-custom-drc-rule-implementation",children:(0,r.jsx)(n.strong,{children:"Best Practices for Custom DRC Rule Implementation"})}),"\n",(0,r.jsxs)(n.h5,{id:"1-targeted-rule-application",children:["1. ",(0,r.jsx)(n.strong,{children:"Targeted Rule Application"})]}),"\n",(0,r.jsx)(n.p,{children:"Ensure that custom DRC rules are applied only to the relevant parts of the design. For example, if you're enforcing additional clearance for high-voltage nets, ensure that the rule doesn't apply to low-voltage nets or signal traces where it's not necessary."}),"\n",(0,r.jsxs)(n.h5,{id:"2-integration-with-existing-drc",children:["2. ",(0,r.jsx)(n.strong,{children:"Integration with Existing DRC"})]}),"\n",(0,r.jsx)(n.p,{children:"Custom rules should complement the existing DRC checks in KiCad, not replace them. Make sure your custom rules do not conflict with the built-in DRC rules. Ideally, run the built-in DRC first, and then apply custom rules afterward to catch any specialized constraints that KiCad might not detect."}),"\n",(0,r.jsxs)(n.h5,{id:"3-modular-scripting",children:["3. ",(0,r.jsx)(n.strong,{children:"Modular Scripting"})]}),"\n",(0,r.jsx)(n.p,{children:"For complex projects, it\u2019s a good idea to modularize your custom DRC scripts. Break down the different types of checks (e.g., high-voltage clearance, thermal management, RF routing) into separate functions. This makes it easier to maintain and update the scripts as the design evolves."}),"\n",(0,r.jsxs)(n.h5,{id:"4-test-the-script-on-small-sections-first",children:["4. ",(0,r.jsx)(n.strong,{children:"Test the Script on Small Sections First"})]}),"\n",(0,r.jsx)(n.p,{children:"Before applying a custom DRC rule across the entire board, test it on a smaller section or a specific area of the design. This allows you to validate the rule and ensure that it\u2019s correctly identifying violations without causing unnecessary slowdowns or false positives in large designs."}),"\n",(0,r.jsxs)(n.h5,{id:"5-error-reporting",children:["5. ",(0,r.jsx)(n.strong,{children:"Error Reporting"})]}),"\n",(0,r.jsx)(n.p,{children:"Ensure that your custom DRC script provides clear and detailed error messages. When a rule is violated, the script should indicate the exact location on the board and provide a suggestion for how to fix the issue. This minimizes debugging time and helps the designer quickly address problems."}),"\n",(0,r.jsx)(n.hr,{}),"\n",(0,r.jsx)(n.h4,{id:"advanced-custom-drc-example-rf-signal-integrity-check",children:(0,r.jsx)(n.strong,{children:"Advanced Custom DRC Example: RF Signal Integrity Check"})}),"\n",(0,r.jsx)(n.p,{children:"In designs involving RF signals, maintaining signal integrity is crucial. Python scripting allows you to implement custom checks for RF sections of your PCB to ensure that specific routing constraints are followed."}),"\n",(0,r.jsx)(n.h5,{id:"example-custom-rule",children:(0,r.jsx)(n.strong,{children:"Example Custom Rule:"})}),"\n",(0,r.jsxs)(n.ul,{children:["\n",(0,r.jsx)(n.li,{children:"Ensure that all traces connected to RF nets maintain a minimum clearance from digital nets to avoid noise coupling."}),"\n",(0,r.jsx)(n.li,{children:"Verify that RF traces maintain a controlled impedance, checking the trace width and the dielectric layer thickness between the signal trace and ground plane."}),"\n"]}),"\n",(0,r.jsx)(n.pre,{children:(0,r.jsx)(n.code,{className:"language-python",children:'def check_rf_signal_integrity(board):\n    # Define RF nets\n    rf_nets = ["RF_NET1", "RF_NET2"]\n\n    # Define the minimum clearance required for RF nets\n    rf_min_clearance = 1.0\n\n    # Get all tracks from the board\n    tracks = board.GetTracks()\n\n    # Loop through each track and check RF rules\n    for track in tracks:\n        net_name = track.GetNetname()\n\n        if net_name in rf_nets:\n            track_clearance = track.GetClearance()\n\n            # Check that clearance meets the RF requirements\n            for other_track in tracks:\n                if other_track != track:\n                    distance = track.GetDistance(other_track)\n\n                    if distance < rf_min_clearance * 1000000:\n                        print(f"DRC Error: RF net {net_name} is too close to another net.")\n                        return False\n\n    print("All RF signal integrity checks passed.")\n    return True\n'})}),"\n",(0,r.jsx)(n.p,{children:"This script ensures that RF traces are properly isolated from other nets and maintain the required clearance. You can easily extend this script to check for other critical parameters, such as trace length matching or via avoidance in sensitive sections."}),"\n",(0,r.jsx)(n.hr,{}),"\n",(0,r.jsx)(n.h4,{id:"conclusion",children:(0,r.jsx)(n.strong,{children:"Conclusion"})}),"\n",(0,r.jsx)(n.p,{children:"Customizing DRC rules in KiCad through Python scripting provides PCB designers with a powerful tool for enforcing specific design requirements, improving reliability, and automating complex checks that are not covered by default. Whether you're designing for high-voltage applications, RF circuits, or sensitive analog layouts, Python scripts offer the flexibility and precision needed to ensure your PCB design meets all necessary constraints."})]})}function d(e={}){const{wrapper:n}={...(0,s.R)(),...e.components};return n?(0,r.jsx)(n,{...e,children:(0,r.jsx)(h,{...e})}):h(e)}},8453:(e,n,t)=>{t.d(n,{R:()=>o,x:()=>a});var i=t(6540);const r={},s=i.createContext(r);function o(e){const n=i.useContext(s);return i.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function a(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(r):e.components||r:o(e.components),i.createElement(s.Provider,{value:n},e.children)}}}]);