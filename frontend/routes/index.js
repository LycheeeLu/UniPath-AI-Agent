import express from "express";
const express = require('express');
const router = express.Router();
const axios = require('axios');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

export default router;


router.get('/resume', (req, res) => {
  res.render('resume', { result: null });
});

router.post('/resume', upload.single('resume'), async (req, res) => {
  try {
    const filePath = req.file.path;
    const fs = require('fs');
    const formData = new FormData();
    formData.append('file', fs.createReadStream(filePath));


    const response = await axios.post('http://127.0.0.1:8000/upload-resume', formData, {
      headers: formData.getHeaders()
    });

    res.render('resume', { result: response.data });
  } catch (err) {
    console.error('Upload error:', err.message);
    res.render('resume', { result: { error: 'Upload failed.' } });
  }
});


