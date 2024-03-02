<template>
    <Mwpf3d :mwpf_data="mwpf_data_1" :snapshot_idx="snapshot_idx_interpolated" :camera_scale="5" :width="width"
        :height="width" :top="top">
    </Mwpf3d>
    <Mwpf3d :mwpf_data="mwpf_data_2" :snapshot_idx="snapshot_idx_interpolated" :camera_scale="5" :width="width"
        :height="width" :top="top" :left="2200 - width / 2">
    </Mwpf3d>
    <Mwpf3d :mwpf_data="mwpf_data_3" :snapshot_idx="snapshot_idx_interpolated" :camera_scale="5" :width="width"
        :height="width" :top="top" :left="4400 - width">
    </Mwpf3d>
    <div class="divider" :style="{ left: 1440 + 'px' }"></div>
    <div class="divider" :style="{ left: 4400 - 1440 - 10 + 'px' }"></div>
</template>

<style>
.divider {
    position: absolute;
    width: 5px;
    height: v-bind(width + 'px');
    top: 0;
    background-color: grey;
}
</style>

<script>
import mwpf_3d from './common/mwpf_3d.vue'
import mwpf_textbox from './common/mwpf_textbox.vue'

const steps = 300
const step_duration = 0.15
const duration = (steps + 1) * step_duration

export default {
    props: {
        "scale": { type: Number, default: 1, },
        "time": Number,
        "width": { type: Number, default: 1400, },
        "top": { type: Number, default: 0, },
        "d": { type: Number, default: 5, },
    },
    emits: ["duration-is"],
    data() {
        return {
            mwpf_data_1: null,
            mwpf_data_2: null,
            mwpf_data_3: null,
        }
    },
    components: {
        Mwpf3d: mwpf_3d,
        MwpfTextBox: mwpf_textbox,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // get decoding graph data
        this.mwpf_data_1 = await this.get_data('./common/aps2024_triangle_color_code_example_p0.01.json')
        this.mwpf_data_2 = await this.get_data('./common/aps2024_triangle_color_code_example_p0.02.json')
        this.mwpf_data_3 = await this.get_data('./common/aps2024_triangle_color_code_example_p0.04.json')
        console.log("main component mounted")
        console.log("expected resolution: 4400 * 2000")
    },
    computed: {
        snapshot_idx_interpolated() {
            let time = this.time
            if (time < steps * step_duration) {
                const step_index = Math.floor(time / step_duration)
                const step_internal = time / step_duration - step_index  // [0, 1)
                // return step_index + this.smooth_animate(step_internal)
                return step_index + step_internal
            }
            return steps
        },
    },
    methods: {
        async get_data(json_path) {
            const response = await fetch(json_path, { cache: 'no-cache', })
            const json_value = await response.json()
            // return json_value
            return remove_resolve_steps_from_mwpf_data(json_value)
        },
        smooth_animate(ratio) {
            if (ratio < 0) ratio = 0
            if (ratio > 1) ratio = 1
            if (ratio < 0.5) {
                return 2 * ratio * ratio
            }
            return 1 - 2 * (1 - ratio) * (1 - ratio)
        }
    },
    watch: {

    },
}
</script>
