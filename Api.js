// Import necessary modules
const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const compiler = require("compilex");

// Configuration options for compilex module
const compileOptions = { stats: true };
compiler.init(compileOptions);

// Middleware setup
app.use(bodyParser.json());

// Serve static files (CodeMirror library)
app.use("/codemirror-5.65.16", express.static("R:/suhackthon/hackathon/static/editor/codemirror-5.65.16"));

// Handling GET request for the main page
app.get("/editor", function (req, res) {
    // Flush compiler before serving the page
    compiler.flush(function () {
        console.log("Deleted old compilation files");
    });
    res.sendFile("R:/suhackthon/hackathon/templates/editor.html");
});

// Handling POST request for code compilation and execution
app.post("/editor", function (req, res) {
    try {
        const code = req.body.code;
        const input = req.body.input;
        const lang = req.body.lang;

        if (lang === "Cpp") {
            handleCppCompilation(res, code, input);
        } else if (lang === "Java") {
            handleJavaCompilation(res, code, input);
        } else if (lang === "Python") {
            handlePythonCompilation(res, code, input);
        } else {
            res.status(400).json({ output: "Unsupported language" });
        }
    } catch (e) {
        console.error("Error:", e);
        res.status(500).json({ output: "Internal server error" });
    }
});

// Function to handle C++ compilation
function handleCppCompilation(res, code, input) {
    const envData = { OS: "windows", cmd: "g++", options: { timeout: 10000 } };

    if (!input) {
        compiler.compileCPP(envData, code, function (data) {
            handleCompilationResponse(res, data);
        });
    } else {
        compiler.compileCPPWithInput(envData, code, input, function (data) {
            handleCompilationResponse(res, data);
        });
    }
}

// Function to handle Java compilation
function handleJavaCompilation(res, code, input) {
    const envData = { OS: "windows" };

    if (!input) {
        compiler.compileJava(envData, code, function (data) {
            handleCompilationResponse(res, data);
        });
    } else {
        compiler.compileJavaWithInput(envData, code, input, function (data) {
            handleCompilationResponse(res, data);
        });
    }
}

// Function to handle Python compilation
function handlePythonCompilation(res, code, input) {
    const envData = { OS: "windows" };

    if (!input) {
        compiler.compilePython(envData, code, function (data) {
            handleCompilationResponse(res, data);
        });
    } else {
        compiler.compilePythonWithInput(envData, code, input, function (data) {
            handleCompilationResponse(res, data);
        });
    }
}

// Function to handle the compilation response
function handleCompilationResponse(res, data) {
    if (data.output) {
        res.status(200).json(data);
    } else {
        res.status(200).json({ output: "error" });
    }
}

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
