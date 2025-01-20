"use strict";(self.webpackChunkPCB_Design=self.webpackChunkPCB_Design||[]).push([[5341],{2333:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>c,contentTitle:()=>s,default:()=>m,frontMatter:()=>i,metadata:()=>r,toc:()=>l});const r=JSON.parse('{"id":"Scripts/BOM","title":"Bill of Materials (BOM) Generation","description":"Generating a Bill of Materials (BOM) is a critical part of the PCB design process. The BOM lists all the components required to manufacture the PCB, along with quantities, part numbers, and additional information necessary for procurement and assembly. Python scripting in KiCad offers powerful tools to automate BOM generation, ensuring that the BOM is accurate, well-formatted, and tailored to meet the needs of your specific project, assembly house, or procurement system.","source":"@site/docs/06_Scripts/05_BOM.md","sourceDirName":"06_Scripts","slug":"/Scripts/BOM","permalink":"/STM32-HW-Design-with-KiCAD/docs/Scripts/BOM","draft":false,"unlisted":false,"editUrl":"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/06_Scripts/05_BOM.md","tags":[],"version":"current","sidebarPosition":5,"frontMatter":{},"sidebar":"ScriptSidebar","previous":{"title":"Netlist Manipulation","permalink":"/STM32-HW-Design-with-KiCAD/docs/Scripts/Netlist"},"next":{"title":"Integration with External Tools","permalink":"/STM32-HW-Design-with-KiCAD/docs/Scripts/Integration"}}');var o=t(4848),a=t(8453);const i={},s="Bill of Materials (BOM) Generation",c={},l=[{value:"Why Automate BOM Generation?",id:"why-automate-bom-generation",level:2},{value:"Common Use Cases for BOM Generation",id:"common-use-cases-for-bom-generation",level:2},{value:"1. Generating a Basic BOM",id:"1-generating-a-basic-bom",level:3},{value:"2. Adding Manufacturer Part Numbers and Supplier Information",id:"2-adding-manufacturer-part-numbers-and-supplier-information",level:3},{value:"3. Customized BOM Formats for Assembly Houses",id:"3-customized-bom-formats-for-assembly-houses",level:3},{value:"4. BOM Grouping and Sorting",id:"4-bom-grouping-and-sorting",level:3},{value:"5. Generating Multi-Board BOMs",id:"5-generating-multi-board-boms",level:3},{value:"Step-by-Step Guide: Automating BOM Generation with Python",id:"step-by-step-guide-automating-bom-generation-with-python",level:2},{value:"Step 1: Extract Component Information from the Schematic",id:"step-1-extract-component-information-from-the-schematic",level:3},{value:"Step 2: Add Manufacturer and Supplier Information",id:"step-2-add-manufacturer-and-supplier-information",level:3},{value:"Step 3: Export the BOM to a CSV File",id:"step-3-export-the-bom-to-a-csv-file",level:3},{value:"Step 4: Running the Script",id:"step-4-running-the-script",level:3},{value:"Best Practices for BOM Generation",id:"best-practices-for-bom-generation",level:2},{value:"1. Include Manufacturer Part Numbers",id:"1-include-manufacturer-part-numbers",level:3},{value:"2. Group and Sort Components",id:"2-group-and-sort-components",level:3},{value:"3. Tailor the BOM Format for Different Stakeholders",id:"3-tailor-the-bom-format-for-different-stakeholders",level:3},{value:"4. Update the BOM Regularly",id:"4-update-the-bom-regularly",level:3},{value:"5. Version Control for BOMs",id:"5-version-control-for-boms",level:3},{value:"Advanced Example: Multi-Board BOM Generation",id:"advanced-example-multi-board-bom-generation",level:2},{value:"Conclusion",id:"conclusion",level:2}];function d(e){const n={code:"code",h1:"h1",h2:"h2",h3:"h3",header:"header",hr:"hr",li:"li",p:"p",pre:"pre",ul:"ul",...(0,a.R)(),...e.components};return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(n.header,{children:(0,o.jsx)(n.h1,{id:"bill-of-materials-bom-generation",children:"Bill of Materials (BOM) Generation"})}),"\n",(0,o.jsx)(n.p,{children:"Generating a Bill of Materials (BOM) is a critical part of the PCB design process. The BOM lists all the components required to manufacture the PCB, along with quantities, part numbers, and additional information necessary for procurement and assembly. Python scripting in KiCad offers powerful tools to automate BOM generation, ensuring that the BOM is accurate, well-formatted, and tailored to meet the needs of your specific project, assembly house, or procurement system."}),"\n",(0,o.jsx)(n.p,{children:"Automating the BOM generation process not only saves time but also reduces the chance of errors, especially in complex designs with many components. Python allows you to customize the format, add additional fields like manufacturer part numbers, and integrate with external databases or systems for sourcing components."}),"\n",(0,o.jsx)(n.hr,{}),"\n",(0,o.jsx)(n.h2,{id:"why-automate-bom-generation",children:"Why Automate BOM Generation?"}),"\n",(0,o.jsx)(n.p,{children:"In any PCB design project, manually generating a BOM can be a time-consuming and error-prone task, particularly for designs that involve a large number of components or frequent revisions. Automating this process with Python scripting ensures consistency, reduces human error, and allows you to easily adapt the BOM format for various requirements. Automating BOM generation has several key benefits:"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:"Efficiency: Automating the process saves time by reducing manual data entry, especially when dealing with numerous components."}),"\n",(0,o.jsx)(n.li,{children:"Accuracy: Automatically extracting information from the design ensures that the BOM accurately reflects the components used in the schematic and layout."}),"\n",(0,o.jsx)(n.li,{children:"Customization: You can format the BOM to meet the needs of different stakeholders, such as your assembly house, procurement team, or external suppliers."}),"\n",(0,o.jsx)(n.li,{children:"Integration: Python scripts can integrate with external databases, enabling automatic lookup and insertion of part numbers, pricing, availability, and other supplier-related details."}),"\n",(0,o.jsx)(n.li,{children:"Update Management: BOM scripts can easily be run whenever there is a design change, ensuring that the BOM is always in sync with the latest version of the design."}),"\n"]}),"\n",(0,o.jsx)(n.hr,{}),"\n",(0,o.jsx)(n.h2,{id:"common-use-cases-for-bom-generation",children:"Common Use Cases for BOM Generation"}),"\n",(0,o.jsx)(n.h3,{id:"1-generating-a-basic-bom",children:"1. Generating a Basic BOM"}),"\n",(0,o.jsx)(n.p,{children:"At its simplest, a BOM contains a list of all components used in a design along with their quantities and designators. A Python script can extract this information directly from the design files, ensuring that the BOM accurately reflects the components used in the schematic."}),"\n",(0,o.jsx)(n.p,{children:"Example:"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:"A basic BOM for a small design might list the resistors, capacitors, integrated circuits (ICs), and connectors, along with their quantities, descriptions, and designators (e.g., R1, C2, U3)."}),"\n"]}),"\n",(0,o.jsx)(n.h3,{id:"2-adding-manufacturer-part-numbers-and-supplier-information",children:"2. Adding Manufacturer Part Numbers and Supplier Information"}),"\n",(0,o.jsx)(n.p,{children:"In most cases, a basic BOM is insufficient for procurement. You need to include manufacturer part numbers, supplier information, and sometimes alternate part options. A Python script can either retrieve this information from a local database or query online APIs to populate these fields."}),"\n",(0,o.jsx)(n.p,{children:"Example:"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:"A script could query a component database to automatically fetch the manufacturer part numbers for each resistor and capacitor, or to pull in pricing and availability information from suppliers like Digi-Key or Mouser."}),"\n"]}),"\n",(0,o.jsx)(n.h3,{id:"3-customized-bom-formats-for-assembly-houses",children:"3. Customized BOM Formats for Assembly Houses"}),"\n",(0,o.jsx)(n.p,{children:"Different assembly houses may have specific requirements for BOM formatting. Python scripts allow you to generate BOMs that are tailored to these requirements, ensuring that the assembly house has all the information needed to manufacture your board correctly. This can include adding extra fields such as component placement details, package types, and special handling instructions."}),"\n",(0,o.jsx)(n.p,{children:"Example:"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:"A Python script can generate a BOM with extra columns for SMT (Surface-Mount Technology) package sizes, special assembly notes, and even placement details (e.g., top or bottom layer of the PCB)."}),"\n"]}),"\n",(0,o.jsx)(n.h3,{id:"4-bom-grouping-and-sorting",children:"4. BOM Grouping and Sorting"}),"\n",(0,o.jsx)(n.p,{children:"In larger designs, grouping components by type (e.g., all resistors together) or sorting them by designator can make the BOM more readable and easier to work with. Python scripts can automate this process, allowing you to organize the BOM in the most logical way for your project."}),"\n",(0,o.jsx)(n.p,{children:"Example:"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:"A script could group all resistors and capacitors together, sort them by value, and then list the associated designators for each component. This makes it easier for procurement teams to source parts in bulk."}),"\n"]}),"\n",(0,o.jsx)(n.h3,{id:"5-generating-multi-board-boms",children:"5. Generating Multi-Board BOMs"}),"\n",(0,o.jsx)(n.p,{children:"In designs that involve multiple PCBs or subsystems, generating a unified BOM across all boards can be challenging. Python scripts can automate the merging of BOMs from multiple boards, ensuring that quantities are consolidated, and all necessary components are listed in a single document."}),"\n",(0,o.jsx)(n.p,{children:"Example:"}),"\n",(0,o.jsxs)(n.ul,{children:["\n",(0,o.jsx)(n.li,{children:"For a project involving a main control board and a power distribution board, a script can merge the BOMs from both designs, ensuring that the total number of common components like connectors or resistors is correctly calculated."}),"\n"]}),"\n",(0,o.jsx)(n.hr,{}),"\n",(0,o.jsx)(n.h2,{id:"step-by-step-guide-automating-bom-generation-with-python",children:"Step-by-Step Guide: Automating BOM Generation with Python"}),"\n",(0,o.jsx)(n.p,{children:"Let\u2019s walk through an example of using Python scripting in KiCad to automate the generation of a detailed BOM that includes basic component information along with manufacturer part numbers and supplier details."}),"\n",(0,o.jsx)(n.h3,{id:"step-1-extract-component-information-from-the-schematic",children:"Step 1: Extract Component Information from the Schematic"}),"\n",(0,o.jsxs)(n.p,{children:["The first step in generating a BOM is to extract the relevant information from the schematic. Using KiCad\u2019s ",(0,o.jsx)(n.code,{children:"pcbnew"})," or ",(0,o.jsx)(n.code,{children:"eeschema"})," libraries, you can programmatically access the components and their associated properties."]}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:"import pcbnew\n\ndef extract_components():\n    board = pcbnew.GetBoard()\n    components = board.GetModules()\n\n    bom_data = []\n\n    for component in components:\n        ref = component.GetReference()\n        value = component.GetValue()\n        footprint = component.GetFPID().GetLibItemName()\n        quantity = 1  # Default to 1 for each component\n\n        bom_data.append({\n            'Reference': ref,\n            'Value': value,\n            'Footprint': footprint,\n            'Quantity': quantity\n        })\n\n    return bom_data\n"})}),"\n",(0,o.jsx)(n.h3,{id:"step-2-add-manufacturer-and-supplier-information",children:"Step 2: Add Manufacturer and Supplier Information"}),"\n",(0,o.jsx)(n.p,{children:"Once you have the basic component data, you can extend the script to include additional fields such as manufacturer part numbers and supplier details. These can be retrieved from a local database or external sources."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:"def add_supplier_info(bom_data):\n    for component in bom_data:\n        # Example: Add manufacturer and supplier information\n        if component['Value'] == '10k':\n            component['Manufacturer Part Number'] = 'RES-10K-1%_0805'\n            component['Supplier'] = 'Digi-Key'\n            component['Supplier Part Number'] = '311-10K-RC'\n        else:\n            component['Manufacturer Part Number'] = 'Unknown'\n            component['Supplier'] = 'Unknown'\n\n    return bom_data\n"})}),"\n",(0,o.jsx)(n.h3,{id:"step-3-export-the-bom-to-a-csv-file",children:"Step 3: Export the BOM to a CSV File"}),"\n",(0,o.jsx)(n.p,{children:"The final step is to export the BOM to a CSV file or another format that matches the requirements of your assembly house or procurement system. CSV is a common format that can be easily imported into most procurement tools."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:"import csv\n\ndef export_bom_to_csv(bom_data, filename='bom.csv'):\n    with open(filename, mode='w', newline='') as file:\n        writer = csv.DictWriter(file, fieldnames=bom_data[0].keys())\n        writer.writeheader()\n        for component in bom_data:\n            writer.writerow(component)\n\n    print(f\"BOM exported to {filename}\")\n"})}),"\n",(0,o.jsx)(n.h3,{id:"step-4-running-the-script",children:"Step 4: Running the Script"}),"\n",(0,o.jsx)(n.p,{children:"After writing the script, you can run it directly from KiCad\u2019s Python scripting console or from an external Python environment. This will generate a BOM with all the necessary fields."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:"# Generate the BOM\nbom_data = extract_components()\n\n# Add manufacturer and supplier information\nbom_data = add_supplier_info(bom_data)\n\n# Export to CSV\nexport_bom_to_csv(bom_data, 'my_custom_bom.csv')\n"})}),"\n",(0,o.jsx)(n.hr,{}),"\n",(0,o.jsx)(n.h2,{id:"best-practices-for-bom-generation",children:"Best Practices for BOM Generation"}),"\n",(0,o.jsx)(n.h3,{id:"1-include-manufacturer-part-numbers",children:"1. Include Manufacturer Part Numbers"}),"\n",(0,o.jsx)(n.p,{children:"The inclusion of manufacturer part numbers is critical for ensuring that the correct components are sourced during procurement. This reduces the chance of errors and ensures that the parts ordered are exactly what was specified in the design."}),"\n",(0,o.jsx)(n.h3,{id:"2-group-and-sort-components",children:"2. Group and Sort Components"}),"\n",(0,o.jsx)(n.p,{children:"For easier reading and to facilitate bulk ordering, group similar components together (e.g., group all resistors or capacitors). Sorting the components by designator or value can also make it easier for the procurement team to process the BOM."}),"\n",(0,o.jsx)(n.h3,{id:"3-tailor-the-bom-format-for-different-stakeholders",children:"3. Tailor the BOM Format for Different Stakeholders"}),"\n",(0,o.jsx)(n.p,{children:"Different stakeholders (assembly houses, procurement teams, or suppliers) may have varying requirements for BOM formats. Use Python scripts to customize the format of the BOM to meet these specific needs. For example, assembly houses may need details on component placement, while procurement teams need supplier information."}),"\n",(0,o.jsx)(n.h3,{id:"4-update-the-bom-regularly",children:"4. Update the BOM Regularly"}),"\n",(0,o.jsx)(n.p,{children:"During the design process, components may change due to availability, cost, or design revisions. Automate the generation of BOMs at every major design milestone to ensure that the BOM always reflects the most current version of the design."}),"\n",(0,o.jsx)(n.h3,{id:"5-version-control-for-boms",children:"5. Version Control for BOMs"}),"\n",(0,o.jsx)(n.p,{children:"Treat your BOM as a key project document and place it under version control alongside your PCB design files. This ensures that changes to the design are always accompanied by an updated BOM, reducing the risk of version mismatches."}),"\n",(0,o.jsx)(n.hr,{}),"\n",(0,o.jsx)(n.h2,{id:"advanced-example-multi-board-bom-generation",children:"Advanced Example: Multi-Board BOM Generation"}),"\n",(0,o.jsx)(n.p,{children:"In projects with multiple PCBs, generating a single, unified BOM can streamline the procurement process. The following script demonstrates how to combine BOMs from multiple boards and generate a consolidated BOM."}),"\n",(0,o.jsx)(n.pre,{children:(0,o.jsx)(n.code,{className:"language-python",children:"def merge_boms(boms):\n    merged_bom = {}\n    \n    for bom in boms:\n        for component in bom:\n            ref = component['Reference']\n            if ref in merged_bom:\n                merged_bom[ref]['Quantity'] += component['Quantity']\n            else:\n                merged_bom[ref] = component\n    \n    return list(merged_bom.values())\n\n# Example usage\nboard1_bom = extract_components_from_board('board1.kicad_pcb')\nboard2_bom = extract_components_from_board('\n\nboard2.kicad_pcb')\n\nmerged_bom = merge_boms([board1_bom, board2_bom])\nexport_bom_to_csv(merged_bom, 'merged_bom.csv')\n"})}),"\n",(0,o.jsxs)(n.p,{children:["This script consolidates components from two different PCBs, merging them into a single BOM. The ",(0,o.jsx)(n.code,{children:"merge_boms"})," function ensures that quantities are updated correctly, and the resulting BOM can be exported in the desired format."]}),"\n",(0,o.jsx)(n.hr,{}),"\n",(0,o.jsx)(n.h2,{id:"conclusion",children:"Conclusion"}),"\n",(0,o.jsx)(n.p,{children:"Automating the generation of BOMs using Python in KiCad significantly improves the accuracy, efficiency, and flexibility of your design process. Whether generating simple BOMs for small designs or complex, multi-board BOMs with detailed supplier information, Python scripting provides a powerful toolset for customizing and optimizing this critical step in PCB design. By following best practices and leveraging Python\u2019s capabilities, you can ensure that your BOM is always accurate, up-to-date, and tailored to the specific needs of your project and stakeholders."})]})}function m(e={}){const{wrapper:n}={...(0,a.R)(),...e.components};return n?(0,o.jsx)(n,{...e,children:(0,o.jsx)(d,{...e})}):d(e)}},8453:(e,n,t)=>{t.d(n,{R:()=>i,x:()=>s});var r=t(6540);const o={},a=r.createContext(o);function i(e){const n=r.useContext(a);return r.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function s(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(o):e.components||o:i(e.components),r.createElement(a.Provider,{value:n},e.children)}}}]);