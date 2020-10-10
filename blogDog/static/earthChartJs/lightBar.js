var lightBarTexture = new THREE.TextureLoader().load("../static/textures/lightBar/lightray.png");
var lightBarParticlesTexture = new THREE.TextureLoader().load('../static/textures/lightBar/particles.png');
var renderOrder = 1;

let baseLightBar = function (width, height, color) {
    let rotateGroup = [];

    let plane1 = new THREE.Mesh(new THREE.PlaneGeometry(width/3, height), new THREE.MeshBasicMaterial({
        map: lightBarTexture,
        color: color,
        transparent: true,
        side: THREE.DoubleSide
    }));

    let plane2 = plane1.clone();
    plane2.rotateY(-Math.PI / 2);
    plane1.add(plane2);

    let plane3 = new THREE.Mesh(new THREE.PlaneGeometry(width, height), new THREE.MeshBasicMaterial({
        map: lightBarParticlesTexture,
        color: '#fff',
        transparent: true,
        side: THREE.DoubleSide
    }));
    plane3.rotateY(Math.PI / 4);
    let plane4 = plane3.clone();
    plane4.rotateY(-Math.PI / 2);
    plane3.add(plane4);
    plane3.name = 'barParticle';

    plane1.renderOrder = renderOrder++
    plane2.renderOrder = renderOrder++
    plane3.renderOrder = renderOrder++
    plane4.renderOrder = renderOrder++
    plane1.rotateX(Math.PI);
    plane1.position.set(0, - height / 2, 0);
    plane3.position.set(0, - height / 2, 0);


    plane3.rotateX(Math.PI);
    rotateGroup.push(plane3);
    rotateGroup.push(plane1);


    return rotateGroup
}

