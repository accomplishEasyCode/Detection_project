<template> 
  <el-card class="info-display">
    <h3 class="info-title">信息展示模块</h3>
    <el-table :data="filteredItems" border style="width: 100%" @sort-change="handleSort">
      <!-- 序号列 -->
      <el-table-column label="序号" width="60">
        <template #default="scope">
          {{ scope.$index + 1 }}
        </template>
      </el-table-column>
      <!-- 商品名 -->
      <el-table-column prop="title" label="商品名" sortable="custom"></el-table-column>
      <!-- 价格 -->
      <el-table-column prop="price" label="价格" sortable="custom" width="100">
        <template #default="scope">
          <span>¥{{ scope.row.price }}</span>
        </template>
      </el-table-column>
      <!-- 所属店铺 -->
      <el-table-column prop="merchants" label="所属店铺" sortable="custom"></el-table-column>
      <!-- 商品链接 -->
      <el-table-column prop="link" label="商品链接">
        <template #default="scope">
          <a :href="scope.row.link" target="_blank">查看</a>
        </template>
      </el-table-column>
      <!-- 商品类别 -->
      <el-table-column prop="product_category" label="商品类别"></el-table-column>
      <!-- 是否侵权（筛选功能） -->
      <!-- <el-table-column prop="Authorization" label="是否侵权" sortable="custom"> -->
      <el-table-column prop="Authorization" label="是否侵权" >

        <template #header>
          <!-- 筛选框 -->
          <el-select v-model="selectedAuthorization" placeholder="选择授权状态" style="width: 100%;">
            <el-option label="已授权" value="授权"></el-option>
            <el-option label="侵权" value="侵权"></el-option>
            <el-option label="全部" value=""></el-option> <!-- 用于显示所有数据 -->
          </el-select>
        </template>
        <template #default="scope">
          <el-tag :type="scope.row.Authorization === '授权' ? 'success' : 'danger'">
            <!-- {{ scope.row.Authorization === '授权' ? '已授权' : '侵权' }} -->
            {{ scope.row.Authorization  }}

          </el-tag>
        </template>
      </el-table-column>
    </el-table>
    <el-button type="primary" @click="refreshData" class="refresh-button">
      刷新数据
    </el-button>
  </el-card>
</template>

<script>
// 引入拼音排序库
import Pinyin from 'pinyin';

export default {
  props: {
    items: {
      type: Array,
      default: () => [], // 接收父组件传递的数据
    },
  },
  data() {
    return {
      localItems: [...this.items], // 将 props 的 items 复制到本地
      selectedAuthorization: '', // 用于存储当前选择的授权状态
    };
  },
  computed: {
    // 通过 selectedAuthorization 过滤数据
    filteredItems() {
      if (!this.selectedAuthorization) {
        return this.localItems;  // 如果没有选择筛选条件，返回所有数据
      }
      return this.localItems.filter(item => {
        if (this.selectedAuthorization === '授权') {
          return item.Authorization === '授权'; // 只返回已授权的项
        }
        return item.Authorization !== '授权'; // 返回非授权项（即侵权项）
      });
    },
  },
  watch: {
    items: {
      handler(newItems) {
        this.localItems = [...newItems]; // 当 props 改变时，同步更新 localItems
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    // 拼音排序方法
    getPinyin(str) {
      return Pinyin(str, { style: Pinyin.STYLE_NORMAL }).join('');
    },

    // 排序逻辑
    handleSort({ prop, order }) {
      const multiplier = order === "ascending" ? 1 : -1;

      // 重新设置排序逻辑，确保每次点击时都重新排序
      if (prop === "price") {
        // 价格排序
        this.localItems.sort((a, b) => {
          const priceA = parseFloat(a.price) || 0;
          const priceB = parseFloat(b.price) || 0;
          return (priceA - priceB) * multiplier;
        });
      } else if (prop === "Authorization") {
        // 是否侵权排序
        this.localItems.sort((a, b) => {
          const authA = a.Authorization === "授权" ? 1 : 0;
          const authB = b.Authorization === "授权" ? 1 : 0;
          return (authA - authB) * multiplier;
        });
      } else if (prop === "merchants") {
        // 所属店铺拼音排序
        this.localItems.sort((a, b) => {
          const pinyinA = this.getPinyin(a.merchants);
          const pinyinB = this.getPinyin(b.merchants);
          return (pinyinA > pinyinB ? 1 : (pinyinA < pinyinB ? -1 : 0)) * multiplier;
        });
      } else if (prop === "title") {
        // 商品名拼音排序
        this.localItems.sort((a, b) => {
          const pinyinA = this.getPinyin(a.title);
          const pinyinB = this.getPinyin(b.title);
          return (pinyinA > pinyinB ? 1 : (pinyinA < pinyinB ? -1 : 0)) * multiplier;
        });
      }
    },

    async refreshData() {
      // 调用父组件的刷新逻辑，并更新 localItems
      try {
        this.$emit("refreshData"); // 通知父组件刷新数据
      } catch (error) {
        console.error("刷新数据失败：", error);
      }
    },
  },
};
</script>

<style scoped>
.info-display {
  margin: 20px auto;
}

.info-title {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

.refresh-button {
  margin-top: 20px;
  width: 100%;
}
</style>
