const express = require("express");
const path = require("path");
const cors = require("cors");
const fs = require("fs");

const app = express();
app.use(cors());

// 提供 Svelte 前端
app.use(express.static(path.join(__dirname, "public")));

// 受控提供图片和视频（避免直接访问整个文件夹）
app.use("/files", express.static(path.join(__dirname, "protected_files")));

// API 让前端获取项目列表
app.get("/api/projects", (req, res) => {
  const projects = [
    {
      title: "Project A",
      images: ["/files/project1/image1.jpg", "/files/project1/image2.jpg"],
      video: "/files/project1/demo.mp4",
      downloadLink: "/api/download/project1"
    }
  ];
  res.json(projects);
});

// 受控下载 API，检查文件是否存在
app.get("/api/download/:project", (req, res) => {
  const project = req.params.project;
  const filePath = path.join(__dirname, `protected_files/${project}/source_code.zip`);

  if (!fs.existsSync(filePath)) {
    return res.status(404).send("File not found");
  }

  res.download(filePath, `${project}_source_code.zip`, (err) => {
    if (err) res.status(500).send("Download failed");
  });
});

// 监听端口
const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
