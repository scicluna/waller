Hooks.on("getSceneControlButtons", (controls) => {
    let wallsControl = controls.find((c) => c.name === "walls");
    if (wallsControl) {
        wallsControl.tools.push({
            name: "automap",
            title: "Automap Walls",
            icon: "fas fa-magic",
            onClick: () => startAutomapping(),
            button: true
        });
    }
});

async function startAutomapping() {
    canvas.toBlob(blob => {
        uploadImageToServer(blob).then(wallData => {
            createWallsInFoundry(wallData);
        });
    }, 'image/png');
}

async function uploadImageToServer(imageBlob) {
    const formData = new FormData();
    formData.append('file', imageBlob);

    try {
        const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Network response was not ok.');

        const wallData = await response.json();
        return wallData; // Use this data to create walls in Foundry VTT
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

function createWallsInFoundry(wallData) {
    wallData.walls.forEach(line => {
        const [x1, y1, x2, y2] = line[0];
        
        // You might need to transform these coordinates based on your canvas scale
        const wall = Wall.create({
            c: [x1, y1, x2, y2],
            // Add any other necessary wall properties here
        });
    });
}