
// Imports the JSON File

let req = new Request("results.json");
let obj = {};
let multiMode = false;

let buttons = {
    "chgMode": {
        "name": "Switch to Multi-mode",
        "onclick": chgMode
    }
}

fetch(req).then((resp) => resp.blob()).then((blob) => blob.text()).then((text) => {
    obj = JSON.parse(text);
    createGrid();
});

initControlPanel()

function initControlPanel() {
    let cpl = document.querySelector(".controlPanel");
    if (cpl) {
        Object.keys(buttons).forEach((key) => {
            let btn = document.createElement("button");
            btn.onclick = buttons[key].onclick;
            btn.innerText = buttons[key].name;
            cpl.appendChild(btn);
        });
    }
}

function createGrid() {
    let grid = document.querySelector(".gridContainer");
    // Clear Existing Grid
    while (grid.firstChild) {
        grid.removeChild(grid.firstChild);
    }

    // Build the grid
    let keys = Object.keys(obj).sort((a, b) => {
        return obj[b].length - obj[a].length;
    });
    keys.forEach((key) => {
        let div = document.createElement("div");
        let title = document.createElement("p");
        let subtitle = document.createElement("p");

        // Multi-mode Checkbox
        let checkbox = document.createElement("input");
        checkbox.setAttribute("type", "checkbox");
        if (multiMode) {
            div.appendChild(checkbox);
        }

        div.setAttribute("class", "color");
        if (isTextDark(key)) {
            title.setAttribute("class", "title dark");
            subtitle.setAttribute("class", "subtitle dark");
        } else {
            title.setAttribute("class", "title light");
            subtitle.setAttribute("class", "subtitle light");
        }
        title.innerText = key;
        subtitle.innerText = (obj[key].length) + " Selectors";
        div.appendChild(title);
        div.appendChild(subtitle);
        div.style.backgroundColor = key;
        div.data = {
            "key": key,
            "selected": false
        }
        div.onclick = updateDetails
        grid.appendChild(div);
    });
}

function isTextDark(str) {
    let r = 0;
    let g = 0;
    let b = 0;
    let a = 0;
    let arr = str.substr(5).split(",");
    if (arr.length === 4) {
        r = Number(arr[0].trim());
        g = Number(arr[1].trim());
        b = Number(arr[2].trim());
        a = Number(arr[3].trim());
    }
    return (((r+g+b)/3)/255 >= 0.5) || (a < 128);
}

function updateDetails(e) {
    console.log("Updated Details!", e.target.data);

    if (e.target.data) {
        if (multiMode) {
            let checkbox = e.target.querySelector("input");
            checkbox.checked = e.target.data.selected ? 0 : 1; // Change to what the value is going to be
            if (e.target.data.selected) {
                e.target.data.selected = false;
                removePane(e.target.data.key);
            } else {
                e.target.data.selected = true;
                let pane = addPane(e.target.data.key);
                updateDetailsPane(pane, e.target.data.key);
            }
        } else {
            let details = document.querySelector(".details");
            if (details) {
                updateDetailsPane(details, e.target.data.key);
            } else {
                let details = addPane(e.target.data.key);
                updateDetailsPane(details, e.target.data.key);
            }
        }
    }
}

function chgMode(e) {
    multiMode = !multiMode;
    if (multiMode) {
        e.target.innerText = "Switch to Single-mode";
    } else {
        e.target.innerText = "Switch to Multi-mode";
    }
    removeAllPanes();
    createGrid();
}

function removePane(key) {
    let pc = document.querySelector(".paneContainer");
    if (pc) {
        let children = pc.childNodes;
        for (let i = 0 ; i < children.length; i++) {
            let child = children[i];
            if (child.key === key) {
                pc.removeChild(child);
                return;
            }
        };
    }
}

function removeAllPanes() {
    let pc = document.querySelector(".paneContainer");
    while (pc.firstChild) {
        pc.removeChild(pc.firstChild)
    }
}

function addPane(key) {
    let pc = document.querySelector(".paneContainer");
    if (pc) {
        let pane = document.createElement("div");
        pane.setAttribute("class", "details");
        pane.key = key;
        pc.appendChild(pane);
        return pane;
    }
}

// Updates a single Pane for viewing the Color Details
function updateDetailsPane(elem, key) {
    // Delete the old children
    while (elem.firstChild) {
        elem.removeChild(elem.firstChild);
    }

    // Add New Title
    let title = document.createElement("div");
    if (isTextDark(key)) {
        title.setAttribute("class", "title dark");
    } else {
        title.setAttribute("class", "title light");
    }
    title.style.backgroundColor = key;
    let titleHeader = document.createElement("h1");
    titleHeader.innerText = key;
    title.appendChild(titleHeader);
    elem.appendChild(title);

    // Add new selectors
    obj[key].forEach((item) => {
        let sel = document.createElement("div");
        sel.setAttribute("class", "selector");
        let code = document.createElement("code");
        code.innerText = item;
        sel.appendChild(code);
        sel.style.borderLeftColor = key;
        elem.appendChild(sel);
    });
    elem.key = key;
}