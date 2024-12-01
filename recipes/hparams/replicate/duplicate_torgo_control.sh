#!/bin/bash

# Base YAML file name
base_yaml="transfer_torgo_control.yaml"

# Base output folder path prefix (excluding freeze configuration)
base_output_folder="results/transfer_control_torgo_"

# Loop for decoder configurations
for i in {1..4}; do
    new_yaml="${base_yaml%.yaml}_freezeD${i}.yaml"
    cp $base_yaml $new_yaml
    echo "Editing $new_yaml..."
    sed -i -e "s|freeze_num_decoder_layers: 0|freeze_num_decoder_layers: ${i}|" \
           -e "s|output_folder: !ref results/transfer_control_torgo_x/|output_folder: !ref ${base_output_folder}freezeD${i}/|" $new_yaml
    echo "Created and modified $new_yaml"
done

# Similarly, repeat for encoder configurations if needed
for i in {1..12}; do
    new_yaml="${base_yaml%.yaml}_freezeE${i}.yaml"
    cp $base_yaml $new_yaml
    sed -i -e "s|freeze_num_encoder_layers: 0|freeze_num_encoder_layers: ${i}|" \
           -e "s|output_folder: !ref results/transfer_control_torgo_x/|output_folder: !ref ${base_output_folder}freezeE${i}/|" $new_yaml
    echo "Created and modified $new_yaml"
done

