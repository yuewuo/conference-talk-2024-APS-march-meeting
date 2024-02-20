<template>
    <div class="textbox" v-if="mwpf_data != null">
        <div v-for="(node, node_index) in dual_nodes">
            <div class="node" :style="{ 'opacity': node.opacity }">
                <span class="node-name" v-html="dual_name(node_index)"
                    :style="{ 'background-color': node.background }"></span>
                <span class="node-value" :style="{ 'opacity': node.value_opacity }" v-html="dual_value(node)"></span>
                <span class="key" v-pre>
                    <math v-pre>
                        <mo>, </mo>
                        <mo>(</mo>
                        <msub>
                            <mi>V</mi>
                            <mi>S</mi>
                        </msub>
                        <mo>,</mo>
                        <msub>
                            <mi>E</mi>
                            <mi>S</mi>
                        </msub>
                        <mo>)</mo>
                        <mo>=</mo>
                    </math>
                </span>
                <div class="mwpf-holder">
                    <Mwpf3d :mwpf_data="mwpf_data" :highlight_vertices="node.v" :highlight_edges="node.e"
                        :camera_scale="camera_scale" :width="size * 2.2" :height="size * 2.2" :top="-size * 1.45">
                    </Mwpf3d>
                </div>
                <span class="key" v-pre>
                    <math v-pre>
                        <mo>, </mo>
                        <mi>&delta;(S)</mi>
                        <mo>=</mo>
                    </math>
                </span>
                <div class="mwpf-holder">
                    <Mwpf3d :mwpf_data="mwpf_data" :highlight_edges="node.h" :camera_scale="camera_scale"
                        :width="size * 2.2" :height="size * 2.2" :top="-size * 1.45">
                    </Mwpf3d>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.textbox {
    position: absolute;
    transform-origin: top left;
    top: v-bind(top + 'px');
    left: v-bind(left + 'px');
    width: v-bind(width + 'px');
    height: v-bind(height + 'px');
    /* background-color: red; */
    font-family: Sans-Serif;
    font-size: v-bind(size + 'px');
    padding-top: v-bind(size + content_top + 'px');
}

.node {
    margin-bottom: v-bind(size + 'px');
    padding-left: v-bind(padding_left + 'px');
}

.node-name {
    padding: v-bind(size * 0.1 + 'px');
    height: v-bind(size + 'px');
    border-radius: v-bind(size * 0.2 + 'px');
    border: solid v-bind(size * 0.05 + 'px') black;
}

.node-value {
    display: inline-block;
    position: relative;
    height: v-bind(size + 'px');
    margin-left: v-bind(size * 0.2 + 'px');
    top: v-bind(-size * 0.2 + 'px');
    width: v-bind(size * 2.5 + 'px');
    font-size: v-bind(size * 0.7 + 'px');
    padding: v-bind(size * 0.1 + 'px');
}

.key {
    position: relative;
    top: v-bind(-size * 0.3 + 'px');
    font-size: v-bind(size * 0.5 + 'px');
}

.mwpf-holder {
    position: relative;
    display: inline-block;
    width: v-bind(size * 2.1 + 'px');
}
</style>

<script async>
import mwpf_3d from './mwpf_3d.vue'

const node_colors = [
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
function lerpColors(color1, color2, ratio) {
    let c1 = new THREE.Color(color1)
    let c2 = new THREE.Color(color2)
    let c = new THREE.Color().lerpColors(c1, c2, ratio)
    return "#" + c.getHexString()
}
function get_node_color(node_index) {
    return node_colors[node_index % node_colors.length]
}

export default {
    props: {
        "top": { type: Number, default: 0, },
        "left": { type: Number, default: 2000, },
        "width": { type: Number, default: 2400, },
        "height": { type: Number, default: 2000, },
        "size": { type: Number, default: 180, },
        "padding_left": { type: Number, default: 0, },
        "animate_duration": { type: Number, default: 0.2, },
        "value_transition": { type: Number, default: 0.8, },  // transition happens in the middle
        "content_top": { type: Number, default: 0, },
        "mwpf_data": {
            type: Object,
            default: mwpf_data_example,
        },
        "snapshot_idx": { type: Number, default: 0, },  // can be any fractional number, if so, the data is interpolated
        "camera_scale": { type: Number, default: 6, },
    },
    data() {
        return {

        }
    },
    components: {
        Mwpf3d: mwpf_3d,
    },
    mounted() {
    },
    methods: {
        dual_name(node_index) {
            return `<math v-pre>
                <msub>
                    <mi>S</mi>
                    <mn>${node_index}</mn>
                </msub>
            </math>`
        },
        dual_value(node) {
            return `<math v-pre>
                <msub>
                    <mi>y</mi>
                    <mi>S</mi>
                </msub>
                <mo>=</mo>
                <mfrac>
                    <mn>${node.dn}</mn>
                    <mn>${node.dd}</mn>
                </mfrac>
            </math>`
        },
    },
    computed: {
        // dual nodes show up as long as the next snapshot has it
        dual_nodes() {
            if (this.mwpf_data == null) {
                return []
            }
            const mwpf_data = this.mwpf_data
            let snapshot_idx = Math.floor(this.snapshot_idx) + 1
            snapshot_idx = Math.min(snapshot_idx, this.mwpf_data.snapshots.length - 1)
            const snapshot = mwpf_data.snapshots[snapshot_idx][1]
            const current_snapshot_idx = Math.floor(this.snapshot_idx)
            const current_snapshot = mwpf_data.snapshots[current_snapshot_idx][1]
            const round_snapshot_idx = Math.round(this.snapshot_idx)
            const round_snapshot = mwpf_data.snapshots[round_snapshot_idx][1]
            const frac_index = this.snapshot_idx - Math.floor(this.snapshot_idx)
            const dual_nodes = []
            for (let [node_index, node] of snapshot.dual_nodes.entries()) {
                let opacity = 1
                if (frac_index < this.animate_duration) {
                    if (node_index >= current_snapshot.dual_nodes.length) {
                        opacity = frac_index / this.animate_duration
                    }
                }
                const color = get_node_color(node_index)
                const background = lerpColors(color, "white", 0.5)
                // calculate value opacity
                let current_node = null
                if (node_index < current_snapshot.dual_nodes.length) {
                    current_node = current_snapshot.dual_nodes[node_index]
                } else {
                    current_node = {
                        d: 0
                    }
                }
                let value_opacity = 1
                if (current_node.d != node.d) {
                    const frac_half = frac_index < 0.5 ? frac_index : 1 - frac_index
                    if (frac_half >= 0.5 - this.value_transition / 2) {
                        value_opacity = (0.5 - frac_half) / (this.value_transition / 2)
                    }
                }
                const modified_node = {
                    ...node,
                    opacity,
                    value_opacity,
                    color,
                    background,
                }
                // modify the node value
                if (node_index >= round_snapshot.dual_nodes.length) {
                    modified_node.dn = 0
                    modified_node.dd = 1
                } else {
                    const round_node = round_snapshot.dual_nodes[node_index]
                    modified_node.dn = round_node.dn
                    modified_node.dd = round_node.dd
                }
                dual_nodes.push(modified_node)
            }
            return dual_nodes
        },
        snapshot_indices() {
            const snapshot_idx = Math.round(this.snapshot_idx)
            const peer_snapshot_idx = this.snapshot_idx < snapshot_idx ? snapshot_idx - 1 : snapshot_idx + 1
            return [snapshot_idx, peer_snapshot_idx]
        },
        snapshot() {
            const mwpf_data = this.mwpf_data
            const [snapshot_idx, peer_snapshot_idx] = this.snapshot_indices
            return mwpf_data.snapshots[snapshot_idx][1]
        },
        peer_snapshot() {
            const mwpf_data = this.mwpf_data
            const [snapshot_idx, peer_snapshot_idx] = this.snapshot_indices
            return mwpf_data.snapshots[peer_snapshot_idx][1]
        },
    },
}
</script>
