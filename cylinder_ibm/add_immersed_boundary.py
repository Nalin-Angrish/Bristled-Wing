boundary_file = "constant/polyMesh/boundary"

with open(boundary_file, 'r') as f:
    lines = f.readlines()

output_lines = []
inserted = False

# Step 1: Extract startFace of "in" patch
in_start_face = None
inside_in_block = False

for line in lines:
    stripped = line.strip()

    if stripped == "in":
        inside_in_block = True
        continue

    if inside_in_block and "startFace" in stripped:
        # Extract number
        in_start_face = stripped.split()[-1].replace(";", "")
        inside_in_block = False

if in_start_face is None:
    raise ValueError("Could not find startFace for 'in' patch")

# Step 2: Process file
for line in lines:
    stripped = line.strip()

    # Update patch count
    if stripped.isdigit() and not inserted:
        output_lines.append("6\n")
        continue

    # Insert cylinder block after '('
    if stripped == "(" and not inserted:
        output_lines.append(line)

        cylinder_block = [
            "    cylinder\n",
            "    {\n",
            "        type            immersedBoundary;\n",
            "        nFaces          0;\n",
            f"        startFace       {in_start_face};\n",
            "\n",
            "        internalFlow    no;\n",
            "        isWall          yes;\n",
            "    }\n"
        ]

        output_lines.extend(cylinder_block)
        inserted = True
        continue

    output_lines.append(line)

# Write output
with open(boundary_file, 'w') as f:
    f.writelines(output_lines)