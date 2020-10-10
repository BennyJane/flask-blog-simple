'use strict';
import {
  convertColor,
  randomColor,
  baseControls,
  basePlane
} from "./base.js";
import {
  baseLightBar,
  lightBarParticlesTexture
} from "./lightBar.js";
import {
  geographicToVector, getSphereHeightPoints,
  addCircle, moonLine, addTexturePoints, skyTexture, createCloudGrid, cloud
} from "./earthLib.js";
import {mark, positionList} from "./data.js";

var camera, scene, renderer, geometry, secondScene;
var controls;
var H = 0;
const DEFAULT = true;
var params = new (function () {
  this.earthSpeed = 1;
  this.ambientLight = DEFAULT; //环境光
  this.directionalLight = false; //平行光
  this.pointLight = false; //点光源
  this.showEarthCopy = DEFAULT; //显示外层透明地球
  this.showLayer = DEFAULT; //添加 遮罩层
  this.showFlyLine = DEFAULT; // 是否显示飞线
  this.showEarthLine = DEFAULT; // 是否显示地球线(真正的渐变线条)
  this.showParticle = DEFAULT; //是否显示粒子特效的粒子(线)
// this.showOuterPoints = false //添加外层粒子
  this.showOuterPoints = DEFAULT; //添加外层粒子
  this.usePass = DEFAULT; //后期处理
  this.strength = 0.05; //处理强度
  this.showDots = true;
  this.showLines = true;
  this.minDistance = 50;
  this.limitConnections = false;
  this.maxConnections = 14;
  this.particleCount = 440;
})();
var R = 200; // 地球半径
var outGap = 30; // 内外球体之间的距离
let moonGroup = new THREE.Group();
let pointsOfMoonline = [];
var range = 1000; //粒子运动边界
let circleNum = 0; // 球体表面圆形的数量
var COUNT = 300; // 遮罩层 单位数量
var loader = new THREE.TextureLoader();
var light = {};
var flyLines = [];
var flyLinesGroup = new THREE.Group();
var earthParticles = new THREE.Object3D();
var earth,
  earthCopy,
  outPointCloud,
  group,
  positions,
  colors,
  particles,
  pointCloud,
  particlePositions,
  linesMesh;
var earthLine = new THREE.Group();
var allGroup = new THREE.Group();
var lightCross = new THREE.Group();
var number = 0;
var particlesData = [];
// maxParticleCount, particleCount 控制外部动态线\点的数量
var maxParticleCount = 400;
var particleCount = 400;
let resolution = new THREE.Vector2(
  window.innerWidth,
  window.innerHeight
);
var lightBarList = baseLightBar(3, 10, "#51ff3e");
var clock = new THREE.Clock();

// 添加点击交互事件
let raycaster = new THREE.Raycaster();
let mouse = new THREE.Vector2();
let selectObject = undefined;
let cityPlanes = [];
let cameraMixer;
let cameraDiv = 1.8;
let moveEnd = false;
let rotateStop = false;
let controlsMixer;
// 添加标记,确保当窗口已经放大完毕后,再渲染更新文本


init();
loadFile(function () {
  camera.position.set(450, 450, 450);
  skyTexture(scene);  // 背景贴图
  createCloudGrid(scene, R);
// loadLayer();
  addLight();
  addOutPointCloud();
// addLine();
// addBoxFlyLine();
  addLightPillars();
  scene.add(allGroup);
// 添加地球表面的点
  createEarthParticles();
  addMoon();
});
animate();

function init() {
  // renderer = new THREE.WebGL1Renderer({
  //   canvas: document.getElementById("example"),
  //   antialias: true,
  //   autoClear: true
  // });
  renderer = new THREE.WebGLRenderer({
    antialias: true,
    autoClear: true
  });
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(window.innerWidth, window.innerHeight); //设置Canvas画布大小
  renderer.toneMapping = THREE.ReinhardToneMapping;
// todo 必须打开该阴影，才能生效
  renderer.shadowMapEnabled = true;
  document.getElementById("visual-chart").appendChild(renderer.domElement); //将画布渲染器绑定到新增的dom节点上；

  scene = new THREE.Scene();
// scene.add(new THREE.GridHelper(10, 50))
// fixme 添加雾化效果,
  scene.fog = new THREE.Fog('#000000', 550, 900);

  camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    10,
    1000
  );
  camera.position.set(0, 0, 400);
  camera.lookAt(0, 0, 0);

  scene.add(new THREE.AmbientLight(0xaaaaaa, 1));
// 添加窗口滚动
//   controls = new THREE.TrackballControls(camera);
//   controls.rotateSpeed = 1.0;
//   controls.zoomSpeed = 1.0;
//   controls.panSpeed = 1.0;
//   controls.noZoom = false;  // 允许缩放,动画效果稍微顺畅一些
//   controls.minDistance = 550;
//   controls.maxDistance = 550;


  controls = baseControls(camera, renderer.domElement);
  controls.addEventListener("change", render);
  controls.minDistance = 540;
  controls.maxDistance = 550;
  controls.enabled = true;  // 是否开启交互
  controls.autoRotateSpeed = 1;  // 自转速度

// ========================================== 添加点击事件 ====================================
  window.addEventListener("resize", onWindowResize, false);
// window.addEventListener("click", onDlightray.pngocumentMouseClick, false)
  window.addEventListener('click', onMouseClick, false);
}

// ========================================== 添加物体 ========================================
// ================== add earth
function loadFile(callback) {
// earth_line2
  loader.load("earthImgs/worldMap.png", textureNormal => {
    earth = new THREE.Mesh(new THREE.SphereBufferGeometry(R, 50, 50), new THREE.MeshPhongMaterial({
      transparent: true,
      depthTest: false,
      opacity: 1.0,
      shininess: 80,
      specular: '#00FFA7',
      shadowSide: THREE.DoubleSide,
      // side: THREE.DoubleSide,
      // renderOrder: 0,
      // receiveShadow: false,
      castShadow: false,
      map: textureNormal,
    }));
    // fixme 外部球体遮挡了光柱子
    earthCopy = new THREE.Mesh(new THREE.SphereBufferGeometry(R + outGap, 50, 50), new THREE.MeshPhongMaterial({
      transparent: true,
      depthTest: false,  // 关闭遮挡效果
      opacity: 0.3,
      shadowSide: THREE.BackSide,
      map: textureNormal
    }));

    // allGroup.add(earth, earthCopy);
    allGroup.add(earth);
    // secondScene.add(earthCopy);
    earth.receiveShadow = true;
    earthCopy.visible = params.showEarthCopy;
    callback()
  })
}

// 添加外层球体上的动态的点与线条
function loadLayer() {
  group = new THREE.Group();
  scene.add(group);
  const segments = maxParticleCount * maxParticleCount;
// const segments = maxParticleCount;

// 构造制定长度的数据
  positions = new Float32Array(segments * 3);
  colors = new Float32Array(segments * 3);

  const pMaterial = new THREE.PointsMaterial({
    // 设置点材质
    color: '#07D46E',
    size: 3,
    blending: THREE.AdditiveBlending, // 什么意思 blending 混合
    transparent: true,
    sizeAttenuation: false
  });

  particles = new THREE.BufferGeometry();
  particlePositions = new Float32Array(maxParticleCount * 3);

  const p = new THREE.Vector3();

  for (let i = 1, l = maxParticleCount; i <= l; i++) {
    //  const p = getPos(R+30, Math.PI * 2 * Math.random(), Math.PI * 2 * Math.random())
    // 计算球面上的点 的坐标
    const phi = Math.acos(-1 + (2 * i) / l);
    const theta = Math.sqrt(l * Math.PI) * phi;
    // 球体坐标转化为三维空间坐标 ==> 转化为最外层的点
    p.setFromSphericalCoords(R + 50, phi, theta);

    const x = p.x;
    const y = p.y;
    const z = p.z;
    // 每三位一作为点坐标
    particlePositions[i * 3] = x;
    particlePositions[i * 3 + 1] = y;
    particlePositions[i * 3 + 2] = z;

    // add it to the geometry
    particlesData.push({
      // 修改这个值,调整点移动的速度
      velocity: new THREE.Vector3((-1 + Math.random() * 2) / 5, (-1 + Math.random() * 2) / 5, (-1 + Math.random() * 2) / 5),
      jiao: [phi, theta],
      numConnections: 0
    });

  }
// drawRange: 用于判断几何体的哪个部分需要被渲染, 不应该直接设置, 而是通过 setDrawRange() 设置
  particles.setDrawRange(0, particleCount);
// 通过 setAttribute 添加 attribute 属性；
// 通过 hashmap 存储该几何体相关的属性，hashmap 的 id 是当前 attribute 的名称，值是相应的 buffer。
// 数字3, 表明每3位一组
// ?? setUsage
  particles.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3).setUsage(THREE.DynamicDrawUsage));

// create the particle system
  pointCloud = new THREE.Points(particles, pMaterial);
  group.add(pointCloud);

  const geometry = new THREE.BufferGeometry();

  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3).setUsage(THREE.DynamicDrawUsage));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3).setUsage(THREE.DynamicDrawUsage));

  geometry.computeBoundingSphere(); //计算当前几何体的的边界球形

  geometry.setDrawRange(0, 0);

  const material = new THREE.LineBasicMaterial({
    vertexColors: true,
    blending: THREE.AdditiveBlending,
    transparent: true,
    color: '#07D46E'
  });

  linesMesh = new THREE.LineSegments(geometry, material);
  group.add(linesMesh);

  renderer.outputEncoding = THREE.sRGBEncoding;
}

// 设置外层球体上, 线条的动画
function layerAnimate() {
  let vertexpos = 0;
  let colorpos = 0;
  let numConnected = 0;
  const O = new THREE.Vector3(0, 0, 0);  // 坐标原点

// 初始化点数据中 numConnections
  for (let i = 0; i < particleCount; i++)
    particlesData[i].numConnections = 0;

  for (let i = 0; i < particleCount; i++) {
    // get the particle: 在 loadLayer 中生成的随机偏移量
    const particleData = particlesData[i];
    // 修改球面点的位置, 变化量 由每个坐标数据对应的 particleData中的velocity参数决定
    particlePositions[i * 3] += particleData.velocity.x;
    particlePositions[i * 3 + 1] += particleData.velocity.y;
    particlePositions[i * 3 + 2] += particleData.velocity.z;

    // 创建新的点位置: 移动后的点
    const v = new THREE.Vector3(particlePositions[i * 3], particlePositions[i * 3 + 1], particlePositions[i * 3 + 2]);

    // 控制点 移动的范围: 距离圆点超过55的时候, 坐标反向移动；
    // 位于 区间内的点, 朝向一个方向移动
    if (v.distanceTo(O) > R + 50) {
      // 取负值
      particleData.velocity.x = -particleData.velocity.x;
      particleData.velocity.y = -particleData.velocity.y;
      particleData.velocity.z = -particleData.velocity.z;
    } else if (v.distanceTo(O) < R + 49) {
      particleData.velocity.x = +particleData.velocity.x;
      particleData.velocity.y = +particleData.velocity.y;
      particleData.velocity.z = +particleData.velocity.z;
    }
    // limitConnections:false ； maxConnections: 14 限制每个点的连接最大数量
    if (params.limitConnections && particleData.numConnections >= params.maxConnections)
      continue;

    // Check collision: 判断点是否碰撞, 只需要检测剩余的点是否存在重合就可以了
    for (let j = i + 1; j < particleCount; j++) {

      const particleDataB = particlesData[j];
      if (params.limitConnections && particleDataB.numConnections >= params.maxConnections)
        continue;

      const dx = particlePositions[i * 3] - particlePositions[j * 3];
      const dy = particlePositions[i * 3 + 1] - particlePositions[j * 3 + 1];
      const dz = particlePositions[i * 3 + 2] - particlePositions[j * 3 + 2];
      //计算两个点之间的具体
      const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);
      // minDistance: 50, 距离小于 50的点的处理
      if (dist < params.minDistance) {

        particleData.numConnections++;
        particleDataB.numConnections++;
        // 距离越接近, 透明度越高
        let alpha = 1.0 - dist / params.minDistance;
        // let alpha = 1.0;

        // 更新 positions 与 colors 内的数据
        positions[vertexpos++] = particlePositions[i * 3];
        positions[vertexpos++] = particlePositions[i * 3 + 1];
        positions[vertexpos++] = particlePositions[i * 3 + 2];

        positions[vertexpos++] = particlePositions[j * 3];
        positions[vertexpos++] = particlePositions[j * 3 + 1];
        positions[vertexpos++] = particlePositions[j * 3 + 2];

        colors[colorpos++] = alpha;
        colors[colorpos++] = alpha;
        colors[colorpos++] = alpha;

        colors[colorpos++] = alpha;
        colors[colorpos++] = alpha;
        colors[colorpos++] = alpha;
        //
        numConnected++;
      }
    }
  }

// console.log(numConnected); numConnected * 2
// ?? 该变量值的作用 numConnected: 用于确定那部分需要被渲染
  linesMesh.geometry.setDrawRange(0, numConnected * 2.1);
  linesMesh.geometry.attributes.position.needsUpdate = true;
  linesMesh.geometry.attributes.color.needsUpdate = true;
  pointCloud.geometry.attributes.position.needsUpdate = true;
}

function addLight() {
// 环境光越弱, 光柱的效果越明显
  const ambientLight = new THREE.AmbientLight('#009A65', 1);
  scene.add(ambientLight);

// 添加平行光  ==> 不显示
  const directionalLight = new THREE.DirectionalLight('#009A65', 30);
  directionalLight.position.set(R * 4, R * 4, R * 4);
  scene.add(directionalLight);
// 点光源 ==> 不显示
  const pointLight = new THREE.PointLight("#009A65", 10);
  pointLight.position.set(R * 4, R * 4, R * 4);
  scene.add(pointLight);

// 设置光源的可见性
  ambientLight.visible = params.ambientLight;
  directionalLight.visible = false;  // 不显示
  pointLight.visible = false;  // 不显示

  light.ambientLight = ambientLight;
  light.directionalLight = directionalLight;
  light.pointLight = pointLight
}

// 外部 点点星光效果
function addOutPointCloud() {
// Geometry 作为 BufferGeometry 的替代品, 大型项目用 BufferGeometry
  const geo = new THREE.Geometry();
  /** 绕圈取点 **/
  const vector = new THREE.Vector3();
// l点的数量 500
  for (let i = 1, l = 50; i <= l; i++) {
    // 计算 反余弦弧度值
    const phi = Math.acos(-1 + (2 * i) / l);
    // 计算 平方根
    const theta = Math.sqrt(l * Math.PI) * phi;
    // 生成半径为R + 30 球体上的点
    vector.setFromSphericalCoords(R + outGap, phi, theta);

    const v0 = new THREE.Vector3(vector.x, vector.y, vector.z);
    geo.vertices.push(v0);

    // 根据上面球体上的点, 再随机生成10个点
    for (let j = 0; j < 5; j++) {
      const v1 = v0.clone();
      const v = new THREE.Vector3(v1.x * (1.2 + Math.random() / (j + 1)),
        v1.y * (1.4 + Math.random() / (j + 1)),
        v1.z * (1.3 + Math.random() / (j + 1)));
      geo.vertices.push(v)
    }

  }
  outPointCloud = new THREE.Points(geo, new THREE.PointsMaterial({
    color: '#07D46E',
    size: 6,  // 外部点的尺,寸
    transparent: true, // 透明
    opacity: 0.5
  }));

  outPointCloud.geometry.verticesNeedUpdate = true;

  outPointCloud.visible = params.showOuterPoints;

  allGroup.add(outPointCloud)
}


/**
 * 飞线
 */
function addBoxFlyLine() {
  loader.load("static/earthImgs/red_line_1.png", texture => {
    // 两点之间的动线
    // 起始点
    const v0 = geographicToVector(R + 50, mark.marking[0].pos[0], mark.marking[0].pos[1]);
    mark.marking.forEach((elem, i) => {
      if (i === 0) return;
      const v3 = geographicToVector(R + 50, elem.pos[0], elem.pos[1]);
      const res = getSphereHeightPoints(v0, v3, 20, 120); // 20 和 120 为调控角度 一般 R约大 20越大 越小20越小。
      const curve = new THREE.CubicBezierCurve3(v0, res[0], res[1], v3);
      const geo = new THREE.Geometry();
      console.log(curve.getPoints(50));
      // let allPoints = curve.getPoints(50);
      // for (let point in allPoints) {
      //   let v = new THREE.Vector3();
      //   v.set(point.x, point.y, point.z);
      //   geo.vertices.push(v)
      // }
      geo.vertices = curve.getPoints(50);
      const meshLine = new MeshLine();
      meshLine.setGeometry(geo);
      const line = new THREE.Mesh(meshLine.geometry, new MeshLineMaterial({
        color: '#F1F0F0',
        map: texture,
        useMap: true,
        lineWidth: 7,
        resolution: resolution,
        dashArray: 0.8,  // 破折号之间的长度和间距。(0 -无破折号)
        dashRatio: 0.3, // 定义可见和不可见之间的比率(0 -更可见，1 -更不可见)。
        dashOffset: 0,
        // depthTest:false,
        transparent: true,
        sizeAttenuation: 1, //使线宽不变，不管距离(1个单位是屏幕上的1px)(0 -衰减，1 -不衰减)
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending,
        near: camera.near,
        far: camera.far,
      }));
      flyLines.push(line);
      flyLinesGroup.add(line)
    });
    flyLinesGroup.visible = params.showFlyLine;
    allGroup.add(flyLinesGroup)
  })
}

/**
 *  添加光柱和底座
 */
function addLightPillars() {

  const D_VALUE = 1, // 差值
    HEXAGON_RADIUS = 5, // 底座的半径
    hexagon = new THREE.Object3D(),
    coneImg = 'earthImgs/lightray.png',
    hexagonColor = ["#FFF350", "#FFF350", "#FFFFFF", "#FFFFFF"];

  const countries = mark.marking;

  const texture = new THREE.TextureLoader().load(coneImg);
// 添加光柱和底座
  for (let i = 0, length = countries.length; i < length; i++) {
    let cityName = countries[i].name;
    // 修改柱子与台子的位置
    let position = geographicToVector(R + 1, countries[i].pos[0], countries[i].pos[1]);
    const index = Math.floor(Math.random() * 4);
    addPedestal(position, index, cityName); // 地标
    addLightCross(position, index, texture) // 光锥
  }

  scene.add(lightCross);

//添加底座
  function addPedestal(position, index, name) {
    const color = hexagonColor[index];
    // 生成六边形
    const hexagonLine = new THREE.CircleGeometry(HEXAGON_RADIUS, 6);
    const hexagonPlane = new THREE.CircleGeometry(HEXAGON_RADIUS - D_VALUE, 6);
    const vertices = hexagonLine.vertices;
    vertices.shift(); // 第一个节点是中心点
    const circleLineGeom = new THREE.Geometry();
    circleLineGeom.vertices = vertices;
    const circleLine = new THREE.LineLoop(circleLineGeom, new THREE.MeshBasicMaterial({
      color: color,
      side: THREE.DoubleSide,
      depthTest: true
    }));
    const circlePlane = new THREE.Mesh(hexagonPlane, new THREE.MeshBasicMaterial({
      color: color,
      side: THREE.DoubleSide,
      opacity: 0.5,
      depthTest: true
    }));
    circleLine.position.copy(position);
    circlePlane.position.copy(position);
    // 设置朝向圆点
    circlePlane.lookAt(new THREE.Vector3(0, 0, 0));
    circleLine.lookAt(new THREE.Vector3(0, 0, 0));

    circlePlane.name = name;
    cityPlanes.push(circlePlane);
    hexagon.add(circleLine);
    hexagon.add(circlePlane);
    scene.add(hexagon)
  }

//添加光柱
  function addLightCross(position, index, texture) {
    let // height = Math.random() * 100,
      height = 80,
      geometry = new THREE.PlaneGeometry(HEXAGON_RADIUS * 3, height),
      matrix1 = new THREE.Matrix4;
    const plane1 = new THREE.Mesh(geometry, new THREE.MeshBasicMaterial({
      map: texture,
      color: hexagonColor[index],
      transparent: true,
      depthTest: true,
      opacity: 1,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending
    }));
    matrix1.makeRotationX(Math.PI / 2);
    matrix1.setPosition(new THREE.Vector3(0, 0, height / -2));
    geometry.applyMatrix(matrix1);
    let plane2 = plane1.clone();
    plane2.rotation.z = Math.PI / 2;
    plane1.add(plane2);
    plane1.position.copy(position);
    plane1.lookAt(0, 0, 0);
    lightCross.add(plane1)
  }
}


function createEarthParticles() {
// 必须先创建一个节点, 作为canvas的画板, 绘制点
  const earthImg = document.createElement('img');
  earthImg.src = 'static/earthImgs/earthSpec.png';
// 图片加载后,再绘制图片
  earthImg.onload = () => {
    let earthCanvas = document.createElement('canvas'),
      earthCtx = earthCanvas.getContext('2d');
    // 设置画板的大小
    earthCanvas.width = earthImg.width;
    earthCanvas.height = earthImg.height;
    // 在canvas上绘制图片: 图片实例, 坐标位置(2个参数), 图片尺寸(两个参数)
    earthCtx.drawImage(earthImg, 0, 0, earthImg.width, earthImg.height);
    // 获取图片的像素数据, 每个像素点 对应四个数值: r g b a
    const earthImgData = earthCtx.getImageData(0, 0, earthImg.width, earthImg.height);
    const BLINT_SPEED = 0.05;
    let positions = [];
    let materials = [];
    let sizes = [];
    for (let i = 0; i < 2; i++) {
      positions[i] = {
        positions: []
      };
      sizes[i] = {
        sizes: []
      };
      const mat = new THREE.PointsMaterial({
        size: 4,  // 设置圈的尺寸
        color: new THREE.Color('#00FF6F'),  // 区域点颜色 0x03d98e ,
        map: new THREE.TextureLoader().load("static/earthImgs/dot.png"),
        depthWrite: false,
        depthTest: false,
        transparent: true,
        opacity: 0,  // 透明度为0 , 默认不显示
        side: THREE.FrontSide,
        blending: THREE.AdditiveBlending
      });
      let n = i / 2;
      mat.t_ = n * Math.PI * 2;  // 取值: 0 => 0 ；1=> 2 * pi
      mat.speed_ = BLINT_SPEED;
      mat.min_ = .2 * Math.random() + .5;
      mat.delta_ = .1 * Math.random() + .1;
      mat.opacity_coef_ = 1;
      materials.push(mat)
    }
    // 绘制等大小的球体
    let spherical = new THREE.Spherical();
    spherical.radius = R;
    const step = 230; // 每圈点的密度: 250
    // todo 控制维度方向的圆点的密度, 维度越高, 点的密度越小
    for (let i = 0; i < step; i++) {
      let vec = new THREE.Vector3();
      // let radians = step * (1 - Math.sin(i / step * Math.PI)) / step + .5; // 每个纬线圈内的角度均分
      let radians = (1 - Math.sin(i / step * Math.PI)) + .5; // 每个纬线圈内的角度均分
      for (let j = 0; j < step; j += radians) {
        let c = j / step, // 底图上的横向百分比  ==> 纬度方向的分割: 0~1
          f = i / step, // 底图上的纵向百分比  ==> 经度方向的分割: 0~1
          index = Math.floor(2 * Math.random());  // 随机结果 0 OR 1
        const pos = positions[index];
        const size = sizes[index];
        if (isLandByUV(c, f)) { // 根据横纵百分比判断在底图中的像素值的透明度是否为0
          // 范围: -Math.PI/2 ~ Math.PI * 1.5
          // 必须是这个范围, 否则 点会与下面的图对不上
          spherical.theta = c * Math.PI * 2 - Math.PI / 2; // 横纵百分比转换为theta和phi夹角
          // spherical.theta = c * Math.PI * 2; // 横纵百分比转换为theta和phi夹角
          spherical.phi = f * Math.PI; // 横纵百分比转换为theta和phi夹角
          vec.setFromSpherical(spherical); // 夹角转换为世界坐标
          pos.positions.push(vec.x);
          pos.positions.push(vec.y);
          pos.positions.push(vec.z);
          //
          if (j % 3 === 0) {
            size.sizes.push(6.0)
          }
        } else {
          // fixme 判断花费的时间太多了 ==> 考虑保存坐标,直接添加, 不再判断
          // 填加球体上圆圈
          if (Math.random() < 0.003 && circleNum < 100) {
            circleNum++;
            spherical.theta = c * Math.PI * 2 - Math.PI / 2; // 横纵百分比转换为theta和phi夹角
            // spherical.theta = c * Math.PI * 2; // 横纵百分比转换为theta和phi夹角
            spherical.phi = f * Math.PI; // 横纵百分比转换为theta和phi夹角
            vec.setFromSpherical(spherical); // 夹角转换为世界坐标
            // console.log('vec', vec)
            let circleLine = addCircle(vec);
            earthParticles.add(circleLine);
          }
        }
      }
    }
    for (let i = 0; i < positions.length; i++) {
      let pos = positions[i],
        size = sizes[i],
        bufferGeom = new THREE.BufferGeometry,
        typedArr1 = new Float32Array(pos.positions.length),
        typedArr2 = new Float32Array(size.sizes.length);
      // 将一般的数组转化为 Float32Array
      for (let j = 0; j < pos.positions.length; j++) {
        typedArr1[j] = pos.positions[j]
      }
      for (let j = 0; j < size.sizes.length; j++) {
        typedArr2[j] = size.sizes[j]
      }
      bufferGeom.addAttribute("position", new THREE.BufferAttribute(typedArr1, 3));
      bufferGeom.addAttribute('size', new THREE.BufferAttribute(typedArr2, 1));
      bufferGeom.computeBoundingSphere();
      let particle = new THREE.Points(bufferGeom, materials[i]);
      earthParticles.add(particle)
    }

    function isLandByUV(c, f) {
      if (!earthImgData) { // 底图数据
        console.error('data error!')
      }
      // 根据百分比, 计算图片中对应的坐标
      const n = parseInt(earthImg.width * c); // 横坐标   根据横纵百分比计算图象坐标系中的坐标
      const o = parseInt(earthImg.height * f); //纵坐标   根据横纵百分比计算图象坐标系中的坐标
      // 计算坐标对应像素点的 A-alpha值, 判断透明度是否为0
      // 计算思路: 像素点为整数,(10, 20) 位置的点之前有 10 * 每行像素点数量 + 20
      // 每个像素点 的颜色由 4个数值记录, 所以再乘以4
      return 0 === earthImgData.data[4 * (o * earthImgData.width + n)] // 查找底图中对应像素点的rgba值并判断
    }

    scene.add(earthParticles);
  }
}

function addMoon() {
  let rList = [295, 268,];
  let edgList = [Math.PI, Math.PI * 1.34];
  for (let i in rList) {
    let edg = edgList[i]
    let l = moonLine(rList[i], edg);
    moonGroup.add(l)
  }
  scene.add(moonGroup)
}

function onWindowResize() {
  var width = window.innerWidth;
  var height = window.innerHeight;

  camera.aspect = width / height;
  renderer.setSize(width, height);
  camera.updateProjectionMatrix();
// camera.position.set(450, 450, 450);
  render();
}

function onMouseClick(evnet) {
  event.preventDefault();
  // 通过鼠标点击位置,计算出 raycaster 所需点的位置,以屏幕为中心点,范围 -1 到 1
  // 鼠标文档坐标 转化为 空间坐标
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  getIntersects()
}

// 获取与射线相交的对象数组
function getIntersects() {
  //通过鼠标点击的位置(二维坐标)和当前相机的矩阵计算出射线位置
  raycaster.setFromCamera(mouse, camera);
  // 获取与射线相交的对象数组，其中的元素按照距离排序，越近的越靠前
  let intersects = raycaster.intersectObjects(cityPlanes);
  console.log(intersects);
  if (intersects.length !== 0 && intersects[0].object instanceof THREE.Mesh) {
    let target = intersects[0].object;
    if (target.name !== '') {
      console.log(intersects);
      let meshPositon = target.position;
      selectObject = intersects[0].object;
      controls.minDistance = 200;
      cameraMove(meshPositon);  // 阻塞；动画执行完后才会向后执行
      // controlsChange();
      // 标记是否已经放大
      // selectObject = undefined;
      moveEnd = true;
      controls.autoRotate = false;
      // renderDiv(selectObject);
    }
  } else {
    selectObject = undefined;
    if (moveEnd === true) {
      controls.minDistance = 550;
      // todo 修改为动画，添加过渡效果
      // cameraReset();
      moveEnd = false;
      controls.autoRotate = true;
    }

  }

}


// 调整弹窗的位置
function renderDiv(object) {
  let labelDom = document.getElementById("label");
  if (object !== undefined && controls.autoRotate === false) {
    let halfWidth = window.innerWidth / 2;
    let halfHeight = window.innerHeight / 2;
    // 整个窗口中心点 0.0 ； x右边为正；y向上为正
    let vector = object.position.clone().project(camera);
    labelDom.innerHTML = '国家: ' + object.name;
    // console.log('vector', vector)
    let leftDist = vector.x * halfWidth + halfWidth;
    let topDist = -1 * vector.y * halfHeight + halfHeight;
    labelDom.setAttribute('style', 'left: ' + leftDist + 'px; top : ' + topDist + 'px;')
  } else {
    labelDom.innerHTML = '';
    labelDom.setAttribute('style', 'visible: hidden')
  }
}

// ================================================ 相机运动
//todo 运动过程抖动, 不流畅
function cameraMove(finalPosition) {
  let cameraPosition = camera.position;
  // 添加相机前后运动
  let positions = [
    cameraPosition.x, cameraPosition.y, cameraPosition.z,
    finalPosition.x * cameraDiv, finalPosition.y * cameraDiv, finalPosition.z * cameraDiv,
    // finalPosition.x * cameraDiv, finalPosition.y * cameraDiv, finalPosition.z * cameraDiv,
  ];
  console.log('positions', positions);

  // QuaternionKeyframeTrack( name : String, times : Array, values : Array )
  // 关键帧时间指的是 各个时间点, 而不是持续时间
  let positionKF = new THREE.NumberKeyframeTrack('.position', [0, 2], positions);
  let clip = new THREE.AnimationClip('move', 23, [positionKF]);
  cameraMixer = new THREE.AnimationMixer(camera);
  let actionCamera = cameraMixer.clipAction(clip);
  actionCamera.setLoop(THREE.LoopOnce, 1);
  actionCamera.clampWhenFinished = true;
  actionCamera.play()
}

function cameraReset() {
  let cameraPosition = camera.position;
  console.log('重新调整相机的位置', cameraPosition);
  // 添加相机前后运动
  let positions = [
    cameraPosition.x, cameraPosition.y, cameraPosition.z,
    cameraPosition.x * cameraDiv, cameraPosition.y * cameraDiv, cameraPosition.x * cameraDiv,
  ];
  // QuaternionKeyframeTrack( name : String, times : Array, values : Array )
  // 关键帧时间指的是 各个时间点, 而不是持续时间
  let positionKF = new THREE.NumberKeyframeTrack('.position', [0, 1], positions);
  // let lookKF = new THREE.NumberKeyframeTrack('.lookAt', [0, 3, 10], [0, 0, 0, 0, 0, 0, 0, 0, 0,]);
  let clip = new THREE.AnimationClip('move', 1, [positionKF]);
  cameraMixer = new THREE.AnimationMixer(camera);
  let actionCamera = cameraMixer.clipAction(clip);
  actionCamera.setLoop(THREE.LoopOnce, 1);
  actionCamera.clampWhenFinished = true;
  actionCamera.play()
}


// ========================================== 添加运动事件 ========================================
function animate() {
  render();
  requestAnimationFrame(animate);
  renderDiv(selectObject);
  // 更新controls；放在animate内, 不要放在render里
  controls.update(clock.getDelta());

  // TWEEN.update();
  //外层地球自转  ==> 独立于 controls的自转效果
  if (moonGroup) {
    moonGroup.rotateY(0.002);
    moonGroup.rotateX(0.002);
  }


//飞线动画
  flyLines.forEach(line => line.material.uniforms.dashOffset.value -= 0.01);

//光柱 修改透明度
  if (lightCross) {
    number = number + 0.01;
    lightCross.traverse(e => {
      if (e.isMesh) {
        e.material.opacity = Math.abs(Math.sin(number)) + 0.3
      }
    })
  }

// 球面粒子闪烁: 必须添加该动画,地区内的圆点才会显示 ==> 默认为透明的
  let objects = earthParticles.children;
  objects.forEach(obj => {
    let material = obj.material;
    material.t_ += material.speed_;
    // opacity_coef_=1
    // 动态变化点的透明度
    material.opacity = (Math.sin(material.t_) * material.delta_ + material.min_) * material.opacity_coef_ + 0.2;
    // 更新材质
    material.needsUpdate = true
  })
}

function render() {
  let delta = clock.getDelta();
  // controls.update(delta)

  if (cameraMixer) {
    cameraMixer.update(delta)
  }

  // if (controlsMixer) {
  //   controlsMixer.update(delta)
  // }
  renderer.render(scene, camera);
}
