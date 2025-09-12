const basicInfo = {
    currentPath: null,
    currentFileList: [],
    selectedFiles: [],
    currentOpenBar: null,
    currentFilters: {},
};

class sideBarTool {
    constructor(btnID, barID) {
        this.btn = document.querySelector(btnID);
        this.bar = document.querySelector(barID);
        this.btn.addEventListener("click", this.handleClick.bind(this));
    }

    handleClick() {
        if (this.bar.classList.contains("open")) {
            this.fechar();
            basicInfo.currentOpenBar = null;
        }
        else {
            if (basicInfo.currentOpenBar) {
                basicInfo.currentOpenBar.fechar();
            }
            this.abrir();
            basicInfo.currentOpenBar = this;
        }
    }

    abrir() {
        this.bar.classList.add("open");
        mainContent.classList.add("shrink");
    }    

    fechar() {
        this.bar.classList.remove("open");
        mainContent.classList.remove("shrink");
    }    
}

async function openDir() {
    basicInfo.currentFileList = [];
    const pathList = await window.pywebview.api.abrir_pasta();
    let path = await pathList[0];
    basicInfo.currentPath = path;
    pathDisplay.setAttribute("placeholder", basicInfo.currentPath);
    pathDisplay.setAttribute("title", basicInfo.currentPath);
    let files = await window.pywebview.api.pesquisa_simples(path);
    basicInfo.currentFileList = files;
    await carregarArquivos();
}

async function carregarArquivos() {
    fileInfo.innerHTML = "";
    basicInfo.selectedFiles = [];

    for (let file of basicInfo.currentFileList) {
        const ul = document.createElement("ul");
        
        for (let [key, value] of Object.entries(file)) {
            if(key === "path") {
                continue;
            }
            const li = document.createElement("li");
            li.setAttribute("class", key);
            li.textContent = value;
            ul.appendChild(li);
        }

        ul.addEventListener("click", () => {
            if (!basicInfo.selectedFiles.includes(file)) {
                basicInfo.selectedFiles.push(file);
            }
            else {               
                basicInfo.selectedFiles = basicInfo.selectedFiles.filter(f => f !== file);
            }
            
            ul.classList.toggle("selected");
        })

        fileInfo.appendChild(ul);
    }
}


const fileInfo = document.querySelector("#file-info");
const mainContent = document.querySelector("main");


const fileSearch = new sideBarTool("#open-btn", "#path-select");
const pathDisplay = document.querySelector("#path-display");
const openDirBtn = document.querySelector("#open-dir-btn");
openDirBtn.addEventListener("click", openDir);

const filterItems = new sideBarTool("#filter-btn", "#filters");
const filterForm = document.querySelector("#filter-form");
const clearFiltersBtn = document.querySelector("#clear-filters-btn");
filterForm.addEventListener("submit", async (e) => {
    e.preventDefault()

    const data = {
        tags: document.querySelector("#tags").value.split(","),
        extensions: document.querySelector("#extensions").value.split(","),
        tamanho_min: Array.from(document.querySelectorAll("[name='tamanho_min']")).map(input => input.value).join(""),
        tamanho_max: Array.from(document.querySelectorAll("[name='tamanho_max']")).map(input => input.value).join(""),
    }
    basicInfo.currentFilters = data
    basicInfo.currentFileList = await window.pywebview.api.apply_filter(basicInfo.currentPath, data)
    await carregarArquivos()
});

clearFiltersBtn.addEventListener("click", async () => {
    basicInfo.currentFilters = {}
    basicInfo.currentFileList = await window.pywebview.api.pesquisa_simples(basicInfo.currentPath)
    await carregarArquivos()
});

const manageFiles = new sideBarTool("#manage-files-btn", "#manage-files");
const moveFilesBtn = document.querySelector("#move-files-btn");
const copyFilesBtn = document.querySelector("#copy-files-btn");
const deleteFilesBtn = document.querySelector("#delete-files-btn");


moveFilesBtn.addEventListener("click", async () => {
    const toMove = basicInfo.selectedFiles.length > 0 ? basicInfo.selectedFiles : basicInfo.currentFileList;
    let destinationFolder = await window.pywebview.api.abrir_pasta();
    destinationFolder = await destinationFolder[0];

    await window.pywebview.api.move_all(toMove, destinationFolder);
    basicInfo.currentFileList = await window.pywebview.api.pesquisa_simples(basicInfo.currentPath);

    await carregarArquivos();
});

copyFilesBtn.addEventListener("click", async ()=> {
    const toCopy = basicInfo.selectedFiles.length > 0 ? basicInfo.selectedFiles : basicInfo.currentFileList;
    let destinationFolder = await window.pywebview.api.abrir_pasta();
    destinationFolder = await destinationFolder[0];

    await window.pywebview.api.copy_all(toCopy, destinationFolder);
    basicInfo.currentFileList = await window.pywebview.api.pesquisa_simples(basicInfo.currentPath);

    await carregarArquivos();
});

deleteFilesBtn.addEventListener("click", async ()=> {
    const toDel = basicInfo.selectedFiles.length > 0 ? basicInfo.selectedFiles : basicInfo.currentFileList;
    
    await window.pywebview.api.delete_all(toDel);

    basicInfo.currentFileList = await window.pywebview.api.pesquisa_simples(basicInfo.currentPath);
    await carregarArquivos();
});

const minimizeBtn = document.querySelector("#minimize-btn")
const restoreBtn = document.querySelector("#restore-btn")
const closeBtn = document.querySelector("#close-btn")

minimizeBtn.addEventListener("click", async () => {
    window.pywebview.api.minimize_window()
})

restoreBtn.addEventListener("click", async () => {
    window.pywebview.api.restore_window()
})

closeBtn.addEventListener("click", async () => {
    window.pywebview.api.close_window()
})