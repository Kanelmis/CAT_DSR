#!/bin/bash

# Base YAML file names
yaml_files=("np2.yaml")

# Base output folder paths
output_folders=("results/transfer_control_np2_")

# Loop over each base YAML and corresponding output folder
for index in ${!yaml_files[@]}; do
    base_yaml=${yaml_files[$index]}
    base_output_folder=${output_folders[$index]}

    # Modify decoder layers and output folder paths
    for i in {1..4}; do
        new_yaml="${base_yaml%.yaml}_freezeD${i}.yaml"
        cp $base_yaml $new_yaml
        sed -i -e "s|freeze_num_decoder_layers: 0|freeze_num_decoder_layers: ${i}|" \
               -e "s|output_folder: !ref ${base_output_folder}x/|output_folder: !ref ${base_output_folder}freezeD${i}/|" $new_yaml
        echo "Modified decoder configuration in $new_yaml"
    done

    # Modify encoder layers and output folder paths
    for i in {1..12}; do
        new_yaml="${base_yaml%.yaml}_freezeE${i}.yaml"
        cp $base_yaml $new_yaml
        sed -i -e "s|freeze_num_encoder_layers: 0|freeze_num_encoder_layers: ${i}|" \
               -e "s|output_folder: !ref ${base_output_folder}x/|output_folder: !ref ${base_output_folder}freezeE${i}/|" $new_yaml
        echo "Modified encoder configuration in $new_yaml"
    done
done

