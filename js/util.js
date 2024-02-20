
function remove_resolve_steps_from_mwpf_data(mwpf_data) {
    const new_data = { ...mwpf_data }
    // filter the snapshots
    const new_snapshots = []
    for (let [label, data] of mwpf_data.snapshots) {
        if (!label.startsWith("resolve ")) {
            new_snapshots.push([label, data])
        }
    }
    new_data.snapshots = new_snapshots
    return new_data
}
