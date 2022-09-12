import React, { useRef, useEffect, useState } from 'react'
import '../App.css';
//import * as THREE from 'three'; // causes warning of duplicate imports of three.js
import * as THREE from "https://unpkg.com/three@0.125.1/build/three.module.js";
// import { OrbitControls } from "https://unpkg.com/three@0.125.1/examples/jsm/controls/OrbitControls.js";

function MCRenderContainer(props) {
    const refContainer = useRef();
    const medicalNote = props.medicalNote;
    const { current: container } = refContainer;
    const [initDone, setInitDone] = useState(false);

    useEffect(() => {
        
        if (medicalNote && container && !initDone) {
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            console.log("Working on " + medicalNote?.entity_extraction + " items")
            const renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            // setRenderer(renderer);
            setInitDone(true);
            container.appendChild(renderer.domElement);

            const geometry = new THREE.BoxGeometry(1, 1, 1);
            const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
            const cube = new THREE.Mesh(geometry, material);
            scene.add(cube);

            camera.position.z = 5;
            function animate() {
                requestAnimationFrame(animate);
                cube.rotation.x += 0.01;
                cube.rotation.y += 0.01;
                renderer.render(scene, camera);
            }
            animate();

        };
    }, [initDone, medicalNote, container]); //, [renderer, setRenderer]



    return (
        <div className="MCRenderContainer" ref={refContainer}>

        </div>
    );

}

export default MCRenderContainer;
