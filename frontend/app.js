import express from "express";
import multer from "multer";
import fetch from "node-fetch";
const upload = multer();
const app = express();

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(express.urlencoded({ extended: true }));

app.get("/", (req, res) => res.render("upload"));

app.post("/upload", upload.single("resume"), async (req, res) => {
  const file = req.file;
  const response = await fetch("http://localhost:8000/upload-resume", {
    method: "POST",
    body: file.buffer,
    headers: { "Content-Type": "application/pdf" },
  });
  const data = await response.json();
  res.render("programs", { resume: data });
});

app.listen(3000, () => console.log("Frontend running on http://localhost:3000"));
