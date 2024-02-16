<template>
    <div class="canvas" ref="canvas_div">

    </div>
</template>

<style scoped>
.canvas {
    /* background-color: lightblue; */
    position: absolute;
    transform-origin: top left;
    top: v-bind(top + 'px');
    left: v-bind(left + 'px');
    width: v-bind(width + 'px');
    height: v-bind(height + 'px');
}
</style>

<script async>

// commonly used vectors
const zero_vector = new THREE.Vector3(0, 0, 0)
const unit_up_vector = new THREE.Vector3(0, 1, 0)

// create common geometries
const segment = 128
const vertex_radius = 0.15
const vertex_geometry = new THREE.SphereGeometry(vertex_radius, segment, segment)
const outline_ratio = 1.2
const vertex_outline_radius = vertex_radius * outline_ratio
const edge_radius = 0.03
export const segmented = Vue.ref(true)
const singular_edge_geometry = new THREE.CylinderGeometry(vertex_radius * 2, vertex_radius * 2, 0.01, segment, 1, false)
singular_edge_geometry.translate(0, -vertex_radius, 0)
const normal_edge_geometry = new THREE.CylinderGeometry(edge_radius, edge_radius, 1, segment, 1, true)
normal_edge_geometry.translate(0, 0.5, 0)
const tri_edge_geometry = new THREE.CylinderGeometry(edge_radius * 1.5, edge_radius * 1.5, 1, segment, 1, true)
tri_edge_geometry.translate(0, 0.5, 0)
const quad_edge_geometry = new THREE.CylinderGeometry(edge_radius * 2, edge_radius * 2, 1, segment, 1, true)
quad_edge_geometry.translate(0, 0.5, 0)
const edge_geometries = [
    singular_edge_geometry,
    normal_edge_geometry,
    tri_edge_geometry,
    quad_edge_geometry,
]
function get_edge_geometry(edge_degree) {
    if (edge_degree - 1 < edge_geometries.length) return edge_geometries[edge_degree - 1]
    return edge_geometries[edge_geometries.length - 1]
}

// create common materials
export const defect_vertex_material = new THREE.MeshStandardMaterial({
    color: 0xff0000,
    opacity: 1,
    transparent: true,
    side: THREE.FrontSide,
})
export const normal_vertex_material = new THREE.MeshStandardMaterial({
    color: 0xffffff,
    opacity: 0.1,
    transparent: true,
    side: THREE.FrontSide,
})
export const defect_vertex_outline_material = new THREE.MeshStandardMaterial({
    color: 0x000000,
    opacity: 1,
    transparent: true,
    side: THREE.BackSide,
})
export const normal_vertex_outline_material = new THREE.MeshStandardMaterial({
    color: 0x000000,
    opacity: 1,
    transparent: true,
    side: THREE.BackSide,
})
export const edge_materials = []
let empty_edge_color = new THREE.Color(0, 0, 0)
let grown_edge_color = new THREE.Color("#D52C1C")
let empty_edge_opacity = 0.1
let grown_edge_opacity = 1
let almost_empty_ratio = 0.1
let almost_grown_ratio = 0.3
let edge_side = THREE.BackSide
const color_steps = 20  // there are 20 colors in the middle apart from the empty and full
export function lerpColors(color1, color2, ratio) {
    let c1 = new THREE.Color(color1)
    let c2 = new THREE.Color(color2)
    let c = new THREE.Color().lerpColors(c1, c2, ratio)
    return "#" + c.getHexString()
}
function make_edge_material(ratio) {
    if (ratio < 0) ratio = 0
    if (ratio > 1) ratio = 1
    return new THREE.MeshStandardMaterial({
        color: lerpColors(empty_edge_color, grown_edge_color, ratio),
        opacity: empty_edge_opacity + (grown_edge_opacity - empty_edge_opacity) * ratio,
        transparent: true,
        side: edge_side
    })
}
edge_materials.push(make_edge_material(0))
edge_materials.push(make_edge_material(1))
for (let i = 0; i < color_steps; ++i) {
    const ratio = almost_empty_ratio +
        (almost_grown_ratio - almost_empty_ratio) * i / (color_steps - 1)
    edge_materials.push(make_edge_material(ratio))
}
function update_edge_materials() {
    for (let idx = 0; idx < color_steps + 2; ++idx) {
        let ratio = almost_empty_ratio +
            (almost_grown_ratio - almost_empty_ratio) * (idx - 2) / (color_steps - 1)
        if (idx == 0) ratio = 0
        if (idx == 1) ratio = 1
        let new_material = make_edge_material(ratio)
        edge_materials[idx].color = new_material.color
        edge_materials[idx].side = new_material.side
        edge_materials[idx].opacity = new_material.opacity
        new_material.dispose()
    }
}
export function get_edge_material(grown, weight) {
    if (grown <= 0 && weight != 0) {  // empty grown
        return edge_materials[0]
    } else if (grown >= weight) {  // fully grown
        return edge_materials[1]
    } else {
        let idx = Math.floor(grown / weight * color_steps)
        if (idx < 0) idx = 0
        if (idx >= color_steps) idx = color_steps - 1
        return edge_materials[idx + 2]
    }
}
export let segmented_edge_colors = [
    "#D52C1C",  // red
    "#44C03F",  // green
    "#2723F7",  // blue
    "#F6C231",  // yellow
    "#4DCCFB",  // light blue
    "#F17B24",  // orange
    "#7C1DD8",  // purple
    "#8C4515",  // brown
    "#E14CB6",  // pink
]
let segmented_untight_opacity = 0.5
let segmented_tight_opacity = 1
export const segmented_edge_materials = []
function update_segmented_edge_materials() {
    for (let [untight, tight] of segmented_edge_materials) {
        untight.dispose()
        tight.dispose()
    }
    segmented_edge_materials.splice(0, segmented_edge_materials.length) // clear
    for (let color of segmented_edge_colors) {
        const tight = new THREE.MeshStandardMaterial({
            color: color,
            opacity: segmented_tight_opacity,
            transparent: true,
            side: edge_side
        })
        const untight = new THREE.MeshStandardMaterial({
            color: color,
            opacity: segmented_untight_opacity,
            transparent: true,
            side: edge_side
        })
        segmented_edge_materials.push([untight, tight])
    }
}
update_segmented_edge_materials()
export function get_segmented_edge_material(is_tight, node_index) {
    return segmented_edge_materials[node_index % segmented_edge_materials.length][is_tight ? 1 : 0]
}
export const subgraph_edge_material = new THREE.MeshStandardMaterial({
    color: 0x0000ff,
    opacity: 1,
    transparent: true,
    side: THREE.FrontSide,
})

// helper functions
export function compute_vector3(data_position) {
    let vector = new THREE.Vector3(0, 0, 0)
    load_position(vector, data_position)
    return vector
}
export function load_position(mesh_position, data_position) {
    mesh_position.z = data_position.i
    mesh_position.x = data_position.j
    mesh_position.y = data_position.t
}



export default {
    props: {
        "top": { type: Number, default: 0, },
        "left": { type: Number, default: 0, },
        "width": { type: Number, default: 2000, },
        "height": { type: Number, default: 2000, },
        "camera_scale": { type: Number, default: 6, },
        "mwpf_data": {
            type: Object,
            default: mwpf_data_example,
        },
        "snapshot_idx": { type: Number, default: 0, },  // can be any fractional number, if so, the data is interpolated
        "highlight_vertices": { type: Object, default: null },
        "highlight_edges": { type: Object, default: null },
    },
    data() {
        return {

        }
    },
    mounted() {
        // create scene
        const scene = new THREE.Scene()
        // scene.background = new THREE.Color(0xff00ff) // debug
        scene.add(new THREE.AmbientLight(0xffffff))
        const aspect_ratio = this.width / this.height
        const camera_scale = this.camera_scale
        const camera = new THREE.OrthographicCamera(- aspect_ratio * camera_scale, aspect_ratio * camera_scale, camera_scale, -camera_scale, 0.1, 100000)
        camera.left = - aspect_ratio * camera_scale
        camera.right = aspect_ratio * camera_scale
        camera.position.x = 0
        camera.position.y = 1000
        camera.position.z = 0
        camera.lookAt(0, 0, 0)
        camera.updateProjectionMatrix()
        this.camera = camera
        scene.add(camera)
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
        renderer.setSize(this.width, this.height, false)
        this.$refs.canvas_div.appendChild(renderer.domElement)
        const canvas = renderer.domElement
        canvas.width = this.width
        canvas.height = this.height
        canvas.style.width = `${this.width}px`
        canvas.style.height = `${this.height}px`
        // orbit control
        const orbit_control = new OrbitControls(camera, renderer.domElement)
        orbit_control.enable = true
        this.orbit_control = orbit_control
        // start animation
        function animate() {
            requestAnimationFrame(animate)
            orbit_control.update()
            renderer.render(scene, camera)
        }
        // meshes that can be reused across different snapshots
        this.variables = {
            scene, renderer, orbit_control,
            vertex_meshes: [],
            vertex_outline_meshes: [],
            edge_vec_meshes: [],
        }
        // refresh data
        this.refresh_snapshot_data()
        animate()
        console.log("mwpf 3d component mounted")
    },
    unmounted() {
        const renderer = this.variables.renderer
        if (renderer != null) {
            renderer.dispose()
            renderer.forceContextLoss()
        }
    },
    computed: {

    },
    methods: {
        get_interpolated_snapshot() {
            const mwpf_data = this.mwpf_data
            const snapshot_idx_1 = Math.floor(this.snapshot_idx)
            const snapshot_idx_2 = snapshot_idx_1 == this.snapshot_idx ? snapshot_idx_1 : snapshot_idx_1 + 1
            const snapshot_1 = mwpf_data.snapshots[snapshot_idx_1][1]
            const snapshot_2 = mwpf_data.snapshots[snapshot_idx_2][1]
            let s1r = snapshot_idx_1 == this.snapshot_idx ? 1 : (snapshot_idx_2 - this.snapshot_idx)
            let s2r = snapshot_idx_1 == this.snapshot_idx ? 0 : (this.snapshot_idx - snapshot_idx_1)
            // interpolate edge
            console.assert(snapshot_1.edges.length == snapshot_2.edges.length)
            const edges = []
            const before_half = s1r > 0.5
            for (let edge_index = 0; edge_index < snapshot_1.edges.length; ++edge_index) {
                const edge1 = snapshot_1.edges[edge_index]
                const edge2 = snapshot_2.edges[edge_index]
                console.assert(edge1.w == edge2.w)
                // console.assert(JSON.stringify(edge1.v) == JSON.stringify(edge2.v))
                const edge = {
                    w: edge1.w,
                    v: edge1.v,
                    g: edge1.g * s1r + edge2.g * s2r,
                    gn: before_half ? edge1.gn : edge2.gn,
                    gd: before_half ? edge1.gd : edge2.gd,
                    un: edge1.un == 0 && edge2.un == 0 ? 0 : 1,
                    ud: 1 // doesn't matter
                }
                edges.push(edge)
            }
            // since dual nodes are never deleted, we can use the snapshot 2 as dual nodes
            const dual_nodes = []
            console.assert(snapshot_1.dual_nodes.length <= snapshot_2.dual_nodes.length)
            for (let node_index = 0; node_index < snapshot_2.dual_nodes.length; ++node_index) {
                const node2 = snapshot_2.dual_nodes[node_index]
                const node1 = node_index < snapshot_1.dual_nodes.length ? snapshot_1.dual_nodes[node_index] : {
                    d: 0,
                    dn: 0,
                    dd: 1,
                }
                const node = {
                    v: node2.v,
                    e: node2.e,
                    h: node2.h,
                    r: node2.r,  // grow rate
                    rn: node2.rn,
                    rd: node2.rd,
                    d: s1r * node1.d + s2r * node2.d,
                    dn: before_half ? node1.dn : node2.dn,
                    dd: before_half ? node1.dd : node2.dd,
                }
                dual_nodes.push(node)
            }
            return {
                edges,
                dual_nodes,
                vertices: snapshot_1.vertices,  // in this version of MWPF, vertices only contains syndrome information
                subgraph: snapshot_1.subgraph,
                'interface': {
                    sum_dual: s1r * snapshot_1.interface.sum_dual + s2r * snapshot_2.interface.sum_dual,
                    sdd: before_half ? snapshot_1.interface.sdd : snapshot_2.interface.sdd,
                    sdn: before_half ? snapshot_1.interface.sdn : snapshot_2.interface.sdn,
                }
            }
        },
        refresh_snapshot_data() {
            if (this.mwpf_data == null) {
                return
            }
            const mwpf_data = this.mwpf_data
            const snapshot = this.get_interpolated_snapshot()
            const { scene, vertex_meshes, vertex_outline_meshes, edge_vec_meshes } = this.variables
            // draw vertices
            for (let [i, vertex] of snapshot.vertices.entries()) {
                if (vertex == null) {
                    if (i < vertex_meshes.length) {  // hide
                        vertex_meshes[i].visible = false
                    }
                    continue
                }
                let position = mwpf_data.positions[i]
                while (vertex_meshes.length <= i) {
                    const vertex_mesh = new THREE.Mesh(vertex_geometry, normal_vertex_material)
                    vertex_mesh.visible = false
                    vertex_mesh.userData = {
                        type: "vertex",
                        vertex_index: vertex_meshes.length,
                    }
                    scene.add(vertex_mesh)
                    vertex_meshes.push(vertex_mesh)
                }
                const vertex_mesh = vertex_meshes[i]
                load_position(vertex_mesh.position, position)
                if (vertex.s) {
                    vertex_mesh.material = defect_vertex_material
                } else {
                    vertex_mesh.material = normal_vertex_material
                }
                vertex_mesh.visible = true
            }
            for (let i = snapshot.vertices.length; i < vertex_meshes.length; ++i) {
                vertex_meshes[i].visible = false
            }
            // draw edges
            let subgraph_set = {}
            if (snapshot.subgraph != null) {
                for (let edge_index of snapshot.subgraph) {
                    subgraph_set[edge_index] = true
                }
            }
            let edge_offset = 0
            if (edge_radius < vertex_outline_radius) {
                edge_offset = Math.sqrt(Math.pow(vertex_outline_radius, 2) - Math.pow(edge_radius, 2))
            }
            for (let [i, edge] of snapshot.edges.entries()) {
                // calculate the center point of all vertices
                let sum_position = new THREE.Vector3(0, 0, 0)
                for (let j = 0; j < edge.v.length; ++j) {
                    const vertex_index = edge.v[j]
                    const vertex_position = mwpf_data.positions[vertex_index]
                    sum_position = sum_position.add(compute_vector3(vertex_position))
                }
                const center_position = sum_position.multiplyScalar(1 / edge.v.length)
                while (edge_vec_meshes.length <= i) {
                    edge_vec_meshes.push([])
                }
                let edge_vec_mesh = edge_vec_meshes[i]
                for (let j = 0; j < edge_vec_mesh.length; ++j) {
                    scene.remove(edge_vec_mesh[j])
                }
                edge_vec_mesh.splice(0, edge_vec_mesh.length) // clear
                const edge_material = get_edge_material(edge.g, edge.w)
                const segmented_dual_indices = []
                if (segmented.value && snapshot.dual_nodes != null) {  // check the non-zero contributing dual variables
                    for (let node_index of this.edge_to_dual_indices[i]) {
                        if (snapshot.dual_nodes[node_index].d != 0) {
                            segmented_dual_indices.push(node_index)
                        }
                    }
                }
                for (let j = 0; j < edge.v.length; ++j) {
                    const create_edge_mesh = () => {
                        const edge_mesh = new THREE.Mesh(get_edge_geometry(edge.v.length), edge_material)
                        edge_mesh.userData = {
                            type: "edge",
                            edge_index: i,
                        }
                        edge_mesh.visible = false
                        scene.add(edge_mesh)
                        return edge_mesh
                    }
                    if (segmented.value) {
                        // the last segment is the empty segment
                        for (let k = 0; k < segmented_dual_indices.length + 1; ++k) {
                            edge_vec_mesh.push(create_edge_mesh())
                        }
                    } else {
                        edge_vec_mesh.push(create_edge_mesh())
                    }
                } for (let j = 0; j < edge.v.length; ++j) {
                    const vertex_index = edge.v[j]
                    const vertex_position = mwpf_data.positions[vertex_index]
                    const relative = center_position.clone().add(compute_vector3(vertex_position).multiplyScalar(-1))
                    const direction = relative.clone().normalize()
                    // console.log(direction)
                    const quaternion = new THREE.Quaternion()
                    quaternion.setFromUnitVectors(unit_up_vector, direction)
                    let start = edge_offset
                    const distance = relative.length()
                    let edge_length = distance - edge_offset
                    if (edge_length < 0) {  // edge length should be non-negative
                        start = distance
                        edge_length = 0
                    }
                    const end = start + edge_length
                    let start_position = compute_vector3(vertex_position).add(relative.clone().multiplyScalar(start / distance))
                    let end_position = compute_vector3(vertex_position).add(relative.clone().multiplyScalar(end / distance))
                    if (edge.v.length == 1) {
                        start_position = compute_vector3(vertex_position)
                        end_position = compute_vector3(vertex_position)
                    }
                    const segment_position_of = (ratio) => {  // 0: start, 1: end
                        return start_position.clone().multiplyScalar(1 - ratio).add(end_position.clone().multiplyScalar(ratio))
                    }
                    if (segmented.value) {
                        // the segmented edges
                        let accumulated_ratio = 0
                        for (let k = 0; k < segmented_dual_indices.length + 1; ++k) {
                            const is_segments = k != segmented_dual_indices.length
                            const edge_mesh = edge_vec_mesh[k * edge.v.length + j]
                            let segment_ratio = 0
                            let node_index = -1
                            if (is_segments) {
                                node_index = segmented_dual_indices[k]
                                const node = snapshot.dual_nodes[node_index]
                                segment_ratio = node.d / edge.w
                            } else {
                                segment_ratio = 1 - accumulated_ratio
                            }
                            edge_mesh.position.copy(segment_position_of(accumulated_ratio))
                            accumulated_ratio += segment_ratio
                            if (edge.v.length != 1) {
                                edge_mesh.scale.set(1, edge_length * segment_ratio, 1)
                                edge_mesh.setRotationFromQuaternion(quaternion)
                            }
                            edge_mesh.visible = true
                            if (edge.v.length != 1 && edge_length * segment_ratio == 0) {
                                edge_mesh.visible = false
                            }
                            edge_mesh.renderOrder = 20 - edge.v.length  // better visual effect
                            if (is_segments) {
                                edge_mesh.material = get_segmented_edge_material(edge.un == 0, node_index)
                            } else {
                                edge_mesh.material = get_edge_material(0, edge.w)
                            }
                            if (snapshot.subgraph != null) {
                                edge_mesh.material = get_edge_material(0, edge.w)  // do not display grown edges
                            }
                            if (subgraph_set[i]) {
                                edge_mesh.material = subgraph_edge_material
                            }
                        }
                    } else {
                        const edge_mesh = edge_vec_mesh[j]
                        edge_mesh.position.copy(start_position)
                        if (edge.v.length != 1) {
                            edge_mesh.scale.set(1, edge_length, 1)
                            edge_mesh.setRotationFromQuaternion(quaternion)
                        }
                        edge_mesh.visible = true
                        if (edge.v.length != 1 && edge_length == 0) {
                            edge_mesh.visible = false
                        }
                        edge_mesh.renderOrder = 20 - edge.v.length  // better visual effect
                        if (snapshot.subgraph != null) {
                            edge_mesh.material = get_edge_material(0, edge.w)  // do not display grown edges
                        }
                        if (subgraph_set[i]) {
                            edge_mesh.material = subgraph_edge_material
                        }
                    }
                }
            }
            for (let i = snapshot.edges.length; i < edge_vec_meshes.length; ++i) {
                for (let edge_mesh of edge_vec_meshes[i]) {
                    edge_mesh.visible = false
                }
            }
            // draw vertex outlines
            for (let [i, vertex] of snapshot.vertices.entries()) {
                if (vertex == null) {
                    if (i < vertex_outline_meshes.length) {  // hide
                        vertex_outline_meshes[i].visible = false
                    }
                    continue
                }
                let position = mwpf_data.positions[i]
                while (vertex_outline_meshes.length <= i) {
                    const vertex_outline_mesh = new THREE.Mesh(vertex_geometry, normal_vertex_outline_material)
                    vertex_outline_mesh.visible = false
                    vertex_outline_mesh.scale.x = outline_ratio
                    vertex_outline_mesh.scale.y = outline_ratio
                    vertex_outline_mesh.scale.z = outline_ratio
                    scene.add(vertex_outline_mesh)
                    vertex_outline_meshes.push(vertex_outline_mesh)
                }
                const vertex_outline_mesh = vertex_outline_meshes[i]
                load_position(vertex_outline_mesh.position, position)
                if (vertex.s) {
                    vertex_outline_mesh.material = defect_vertex_outline_material
                } else if (vertex.v) {
                    vertex_outline_mesh.material = virtual_vertex_outline_material
                } else {
                    vertex_outline_mesh.material = normal_vertex_outline_material
                }
                vertex_outline_mesh.visible = true
            }
            for (let i = snapshot.vertices.length; i < vertex_meshes.length; ++i) {
                vertex_outline_meshes[i].visible = false
            }
            // draw highlights
            if (this.highlight_vertices != null || this.highlight_edges != null) {
                // record original material
                const vertex_meshes_original = []
                const vertex_outline_meshes_original = []
                if (this.highlight_vertices != null) {
                    for (let vertex_index of this.highlight_vertices) {
                        vertex_meshes_original.push(vertex_meshes[vertex_index].material)
                        vertex_outline_meshes_original.push(vertex_outline_meshes[vertex_index].material)
                    }
                }
                // disable all
                const hide_material = get_edge_material(0, 1)
                for (let mesh of vertex_meshes) {
                    mesh.material = hide_material
                }
                for (let mesh of vertex_outline_meshes) {
                    mesh.material = hide_material
                }
                for (let meshes of edge_vec_meshes) {
                    for (let mesh of meshes) {
                        mesh.material = hide_material
                    }
                }
                // recover highlighted material
                if (this.highlight_vertices != null) {
                    for (let [i, vertex_index] of this.highlight_vertices.entries()) {
                        vertex_meshes[vertex_index].material = vertex_meshes_original[i]
                        vertex_outline_meshes[vertex_index].material = vertex_outline_meshes_original[i]
                    }
                }
                if (this.highlight_edges != null) {
                    const highlight_material = get_edge_material(1, 1)
                    for (let [i, edge_index] of this.highlight_edges.entries()) {
                        for (let [j, mesh] of edge_vec_meshes[edge_index].entries()) {
                            mesh.material = highlight_material
                        }
                    }
                }
            }
        },
    },
    watch: {
        snapshot_idx() {
            this.refresh_snapshot_data()
        },
        mwpf_data() {
            this.refresh_snapshot_data()
        },
    },
    computed: {
        edge_to_dual_indices() {
            const snapshot = this.get_interpolated_snapshot()
            const dual_indices = []
            for (let [_, edge] of snapshot.edges.entries()) {
                dual_indices.push([])
            }
            for (let [node_index, node] of snapshot.dual_nodes.entries()) {
                for (let edge_index of node.h) {
                    dual_indices[edge_index].push(node_index)
                }
            }
            return dual_indices
        },
    }
}
</script>
