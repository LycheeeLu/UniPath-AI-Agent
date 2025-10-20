import express from "express";
import multer from "multer";
import fetch from "node-fetch";
import FormData from "form-data";

const upload = multer();
const app = express();

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(express.urlencoded({ extended: true }));

// 🚀 Routes
app.get("/", (req, res) => res.render("upload"));

app.post("/upload", upload.single("resume"), async (req, res) => {
  try {
    const formData = new FormData();
    formData.append("file", req.file.buffer, {
      filename: req.file.originalname,
      contentType: req.file.mimetype,
    });

    const response = await fetch("http://127.0.0.1:8000/upload-resume", {
      method: "POST",
      body: formData,
      headers: formData.getHeaders(),
    });

    const data = await response.json();
    res.render("programs", { resume: data });
  } catch (err) {
    console.error("Upload failed:", err);
    res.render("programs", { resume: { error: "Upload failed." } });
  }
});

app.listen(3000, () =>
  console.log("🌐 Frontend running on http://localhost:3000")
);

app.get("/ping", (req, res) => res.send("pong"));
