<template>
    <Mwpf3d :mwpf_data="mwpf_data" :snapshot_idx="snapshot_idx_interpolated" :camera_scale="2.5"></Mwpf3d>
    <MwpfTextBox :mwpf_data="mwpf_data" :snapshot_idx="snapshot_idx_interpolated" :camera_scale="1.8"></MwpfTextBox>
</template>

<style></style>

<script>
import mwpf_3d from './common/mwpf_3d.vue'
import mwpf_textbox from './common/mwpf_textbox.vue'

const showing = 3
const duration = 4

export default {
    props: {
        "scale": { type: Number, default: 1, },
        "time": Number,
        "d": { type: Number, default: 5, },
    },
    emits: ["duration-is"],
    data() {
        return {
            mwpf_data: null,
        }
    },
    components: {
        Mwpf3d: mwpf_3d,
        MwpfTextBox: mwpf_textbox,
    },
    async mounted() {
        this.$emit('duration-is', duration)
        // get decoding graph data
        let response = await fetch('./common/aps2024_simple_demo.json', { cache: 'no-cache', })
        this.mwpf_data = await response.json()
        console.log("main component mounted")
        console.log("expected resolution: 4400 * 2000")
    },
    computed: {
        snapshot_idx_interpolated() {
            let time = this.time
            let end_index = 1
            if (time < showing) {
                return end_index * this.smooth_animate(time / showing)
            }
            return end_index
        },
    },
    methods: {
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
