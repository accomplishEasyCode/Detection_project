<template>
  <div id="app">
    <el-container>
      <el-header class="app-header">面向电商的商品侵权检测系统</el-header>
      <el-main>
        <!-- 接收来自 InputForm 的关键词和数据 -->
        <InputForm @dataFetched="handleDataFetched" @keywordSubmitted="handleKeyword" />
        <!-- 展示从后端获取的数据 -->
        <InfoDisplay :items="items" @refreshData="refreshItems" />
      </el-main>
    </el-container>

    <!-- 回到顶部按钮 -->
    <div 
      v-show="showBackToTop" 
      class="back-to-top" 
      @click="scrollToTop"
    >
      <ArrowUp />
    </div>
  </div>
</template>

<script>
import InputForm from "./components/InputForm.vue";
import InfoDisplay from "./components/InfoDisplay.vue";
// import new from "./components/new.vue";

import axios from "axios";
import { ArrowUp } from "@element-plus/icons-vue"; // 引入 ArrowUp 图标

export default {
  components: {
    InputForm,
    InfoDisplay,
    ArrowUp, // 注册 ArrowUp 图标
  },
  data() {
    return {
      items: [], // 用于存储商品数据
      keyword: "", // 用户输入的关键词
      target: "", // 用户选择的目标网站
      showBackToTop: false, // 是否显示回到顶部按钮
    };
  },
  methods: {
    // 接收子组件传递的关键词和目标网站
    handleKeyword({ keyword, target }) {
      this.keyword = keyword;
      this.target = target;
      console.log("接收到的关键词：", this.keyword);
      console.log("接收到的目标网站：", this.target);
    },
    handleDataFetched(fetchedData) {
      this.items = fetchedData;
    },
    async refreshItems() {
      if (!this.keyword || !this.target) {
        console.error("关键词或目标网站为空，无法刷新数据！");
        return;
      }
      try {
        console.log("刷新数据，使用的关键词和目标网站为：", this.keyword, this.target);
        const response = await axios.get("/api/get_items", {
          params: 
          { user_text: this.keyword,
            target: this.target 
          },
        });
        this.items = response.data || [];
      } catch (error) {
        console.error("刷新数据失败：", error);
      }
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    handleScroll() {
      this.showBackToTop = window.scrollY > 300;
    },
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>

<style>
.app-header {
  background-color: #409eff;
  color: white;
  text-align: center;
  line-height: 60px;
  font-size: 20px;
  font-weight: bold;
}

.el-main {
  background-color: #f5f5f5;
  padding: 20px;
}

/* 回到顶部按钮样式 */
.back-to-top {
  position: fixed;
  bottom: 40px;
  right: 40px;
  z-index: 1000;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #cfcfcf;
  color: white;
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
}
</style>
