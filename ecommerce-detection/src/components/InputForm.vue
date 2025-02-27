<template>
  <el-card class="input-form">
    <h3 class="form-title">输入关键词和选择目标网站</h3>
    <el-form ref="form" :model="form" label-width="80px" class="form-content">
      <el-form-item label="关键词">
        <el-input v-model="form.keyword" placeholder="请输入关键词"></el-input>
      </el-form-item>
      <el-form-item label="目标网站">
        <el-select v-model="form.target" placeholder="请选择目标网站">
          <el-option label="淘宝" value="taobao"></el-option>
          <el-option label="京东" value="jingdong"></el-option>
        </el-select>
      </el-form-item>
      <div class="button-container">
        <el-button type="primary" @click="startSpider" class="center-button">
          开始检索
        </el-button>
      </div>
    </el-form>
  </el-card>
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      form: {
        keyword: "",
        target: ""
      }
    };
  },
  methods: {
    async startSpider() {
      if (!this.form.keyword || !this.form.target) {
        this.$message.warning("请完整填写关键词和目标网站！");
        return;
      }
      try {
        console.log("发送的参数：", this.form);
        const response = await axios.get("/api/get_items", {
          params: {
            user_text: this.form.keyword,
            target: this.form.target
          }
        });
        this.$message.success("数据获取成功！");
        // 将关键词和目标网站传递给父组件
        this.$emit("keywordSubmitted", { keyword: this.form.keyword, target: this.form.target });
        // 将获取到的数据传递给父组件
        this.$emit("dataFetched", response.data || []); 
      } catch (error) {
        console.error("获取数据失败：", error);
        this.$message.error("获取数据失败，请检查后端连接！");
      }
    }
  }
};
</script>
<style scoped>
.input-form {
  max-width: 600px;
  margin: 0 auto;
}
.form-title {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}
.form-content {
  margin-top: 20px;
}
.button-container {
  text-align: center;
  margin-top: 20px;
}
.center-button {
  width: 150px;
}
</style>