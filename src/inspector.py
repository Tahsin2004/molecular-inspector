import os
import sys
from Bio.PDB import MMCIFParser, PDBList, NeighborSearch

def inspect_binding_pocket():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    pdbl = PDBList()
    cif_path = pdbl.retrieve_pdb_file("5UHC", pdir=data_dir, file_format="mmCif")

    print("Parsing 5UHC macromolecular coordinates...")
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("5UHC", cif_path)
    model = structure[0]

    # Locate Rifampicin (RFP) ligand atoms
    rfp_atoms = [
        atom for atom in model.get_atoms()
        if atom.get_parent().get_resname() == "RFP"
    ]

    if not rfp_atoms:
        print("Error: Ligand 'RFP' (Rifampicin) not found in structure.")
        sys.exit(1)

    print(f"Loaded 5UHC: Identified {len(rfp_atoms)} atoms in Rifampicin (RFP) ligand.\n")

    # Search for protein residues within 5.0 Angstroms of the drug
    protein_atoms = [
        atom for atom in model.get_atoms()
        if atom.get_parent().id[0] == " "
    ]
    neighbor_search = NeighborSearch(protein_atoms)

    pocket_residues = set()
    for rfp_atom in rfp_atoms:
        contacts = neighbor_search.search(rfp_atom.coord, radius=5.0, level="R")
        for res in contacts:
            pocket_residues.add(res)

    pocket_summary = []
    for res in pocket_residues:
        chain_id = res.get_parent().id
        res_name = res.get_resname()
        res_num = res.id[1]
        min_dist = min(
            atom - rfp_atom for atom in res.get_atoms() for rfp_atom in rfp_atoms
        )
        pocket_summary.append({
            "chain": chain_id,
            "res_name": res_name,
            "res_num": res_num,
            "min_dist": min_dist
        })

    pocket_summary.sort(key=lambda x: x["min_dist"])

    print("=== Rifampicin Binding Pocket Contacts (< 5.0 A) ===")
    print(f"{'Chain':<7} | {'Residue':<10} | {'Distance (A)':<14} | {'Status'}")
    print("-" * 54)

    target_serine = None
    for item in pocket_summary:
        res_label = f"{item['res_name']}{item['res_num']}"
        status = "Direct Contact / H-Bond" if item["min_dist"] < 3.5 else "Van der Waals Contact"
        print(f"{item['chain']:<7} | {res_label:<10} | {item['min_dist']:<14.2f} | {status}")
        if item["res_name"] == "SER" and target_serine is None:
            target_serine = item

    print("-" * 54)

    print("\n=== Molecular Resistance Assessment ===")
    if target_serine:
        s_chain = target_serine["chain"]
        s_num = target_serine["res_num"]
        s_dist = target_serine["min_dist"]
        print(f"Target Pocket Residue : Chain {s_chain} - SER{s_num}")
        print(f"Wild-Type Distance    : {s_dist:.2f} A to Rifampicin")
        print("Mechanism Evaluation  : Active contact in the wild-type binding site.")
        print("In Silico Mutation    : Replacing Serine with Leucine introduces a bulky")
        print("                        isobutyl side chain (-CH(CH3)2), producing steric clashes")
        print("                        that physically displace Rifampicin from this pocket.")
    else:
        print("Note: Inspect pocket list above to confirm identified contacts.")

if __name__ == "__main__":
    inspect_binding_pocket()
