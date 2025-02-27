<template>
  <div>
    <!-- 页面内容 -->
    <div style="height: 1500px;">  <!-- 让页面有足够的滚动空间 -->
      <p>这是一个长页面。滚动查看。</p>
    </div>

    <!-- 回到顶部按钮 -->
    <el-button
      icon="el-icon-arrow-up"
      type="primary"
      class="back-to-top"
      @click="scrollToTop"
      v-if="isVisible"
    >
      回到顶部
    </el-button>
  </div>
</template>

<script>
export default {
  name: 'new',
  data() {
    return {
      isVisible: false,  // 控制按钮显示与否
    };
  },
  methods: {
    // 检查滚动位置并显示/隐藏按钮
    handleScroll() {
      if (window.scrollY > 300) {
        this.isVisible = true;
      } else {
        this.isVisible = false;
      }
    },
    // 回到顶部函数
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);  // 监听滚动事件
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);  // 清理事件监听
  },
};
</script>

<style scoped>
.back-to-top {
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: 1000;
}
</style>
