<template>
  <div id="main-container" class="mainContainer">
    <div id="game" class="playingField">
      <div
        v-for="(segment, ind) in snakeCoordinates" 
        class="snake"
        :class="{ head: ind === 0}"
        :style="segment.positionStyle"
        :key="segment.id"
      ></div>
      <div v-if="apple" class="apple" :style="apple.positionStyle"></div>
    </div>
  </div>

    <button type="button" id="pauseButton">Pause</button>

    <form name="dimensions" id="dimensions-form" @submit.prevent="handleFormSubmit">
        <label for="width">Field width:</label>
        <input type="text" id="width" name="width" v-model="fieldWidth" required><br><br>
        <label for="height">Field height:</label>
        <input type="text" id="height" name="height" v-model="fieldHeight" required><br><br>
        <input type="submit" value="Submit">
    </form> 
</template>

<script setup>
import { onMounted, ref } from 'vue';
let fieldWidth = ref(10);
let fieldHeight = ref(10);
const cellSizePx = 50;
const turns = [];
const turnDirections = [];
const cycleDurationMs = 250;
const snakeCoordinates = ref([]);
let headRotationStyle;
let gameCycle;

const opposites = {
    'left': 'right',
    'right': 'left',
    'up': 'down',
    'down': 'up',
};

const rotationStyles = {
    'left': "transform: rotate(270deg)",
    'right': "transform: rotate(90deg)",
    'up': "transform: rotate(0deg)",
    'down': "transform: rotate(180deg)",
};


let direction,
    newDirection;

const apple = ref({});

function handleFormSubmit() {
    resizeField();
        restartGame();
        const pauseButton = document.getElementById('pauseButton');
        if (pauseButton.innerText === 'Resume') {
            clearInterval(gameCycle);
        }
}

function resizeField() {
    const field = document.getElementById('game');
    field.style.cssText += `
        width: ${cellSizePx * fieldWidth.value}px;
        height: ${cellSizePx * fieldHeight.value}px;
        grid-template-rows: repeat(${fieldHeight.value}, 1fr);
        grid-template-columns: repeat(${fieldWidth.value}, 1fr);
    `;
}

function spawn() {
    snakeCoordinates.value.push(
        {x: 1,
        y: 0,
        direction: 'right'},
        {x: 0,
        y: 0,
        direction: 'right',});

    for (let segment of snakeCoordinates.value) {
        segment.positionStyle = `grid-area: ${segment.y + 1} / ${segment.x + 1} / span 1 / span 1;`
    }
    let head = snakeCoordinates.value[0];
    headRotationStyle = rotationStyles[head.direction];
    head.positionStyle += headRotationStyle;      
}

function respawnApple() {
    let x, y;
    do {
        x = Math.floor(Math.random() * fieldWidth.value);
        y = Math.floor(Math.random() * fieldHeight.value);
    } while (snakeCoordinates.value.find(item => item.x === x && item.y === y));
    apple.value.x = x;
    apple.value.y = y;
    apple.value.positionStyle = `grid-area: ${apple.value.y + 1} / ${apple.value.x + 1} / span 1 / span 1;`
}

function elongateSnek(x, y, direction) {
    snakeCoordinates.value.push({
        x,
        y,
        direction,
        positionStyle: `grid-column: ${x + 1} / span 1; grid-row: ${y + 1} / span 1;`
    });
}

function moveSnek() {
    let head = snakeCoordinates.value[0];
    headRotationStyle = rotationStyles[head.direction];
    head.positionStyle += headRotationStyle;
    newDirection = turnDirections.shift();

    if (newDirection != undefined && newDirection != opposites[head.direction] && newDirection != direction) {
        direction = newDirection;
        turns.push({x: head.x, y: head.y, direction: direction});
    }

    if (turns.length > 0) {
        for (let i = turns.length - 1; i >= 0; i--) {
            let turn = turns[i];
            let snakeBend = snakeCoordinates.value.find(item => item.x === turn.x && item.y === turn.y);
            if (snakeBend === undefined) {
                turns.shift();
            } else {
                snakeBend.direction = turn.direction;
            }
        }
    }

    let {x, y, direction: tail_direction} = snakeCoordinates.value.at(-1);

    snakeCoordinates.value.forEach((segment, index) => {
        if (segment.direction === 'left') {
            segment.x--;
        } else if (segment.direction === 'right') {
            segment.x++;
        } else if (segment.direction === 'up') {
            segment.y--;
        } else if (segment.direction === 'down') {
            segment.y++;
        }
        segment.positionStyle = `grid-area: ${segment.y + 1} / ${segment.x + 1} / span 1 / span 1;`
        if (index === 0) {
            headRotationStyle = rotationStyles[head.direction];
            head.positionStyle += headRotationStyle;
        }
    })
    
    if (head.x >= fieldWidth.value || head.y >= fieldHeight.value || head.x < 0 || head.y < 0 ||
        snakeCoordinates.value.filter(item => item.x === head.x && item.y === head.y).length > 1
    ) {
        gameOver();
    }

    if (head.x === apple.value.x && head.y === apple.value.y) {
        elongateSnek(x, y, tail_direction);
        respawnApple();
    }
}

function gameOver() {
    clearInterval(gameCycle);
    let restart = confirm("Game Over. Try again?");
    if (restart) {
        restartGame();
    }
}

function restartGame() {
    snakeCoordinates.value.length = 0;
    spawn();
    gameCycle = setInterval(() => {
        moveSnek();
    }, cycleDurationMs);
}

function pause() {
    const pauseButton = document.getElementById('pauseButton');
    const pauseUnpause = function() {
        if (pauseButton.innerText === 'Pause') {
            clearInterval(gameCycle);
            pauseButton.innerText = 'Resume';
        }
        else {
            gameCycle = setInterval(() => {
                moveSnek();
            }, cycleDurationMs);
            pauseButton.innerText = 'Pause';
        }
    }
    pauseButton.addEventListener('click', pauseUnpause);
}

document.addEventListener('keydown', (event) => {
    if (event.code === 'ArrowDown') {
        newDirection = 'down';
    } else if (event.code === 'ArrowUp') {
        newDirection = 'up';
    } else if (event.code === 'ArrowLeft') {
        newDirection = 'left';
    } else if (event.code === 'ArrowRight') {
        newDirection = 'right';
    }

    turnDirections.push(newDirection);
});

onMounted(() => {
    spawn();
    respawnApple();
    pause();
    gameCycle = setInterval(() => {
    moveSnek();
}, cycleDurationMs);
})
</script>

<style>
.mainContainer {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
}

.playingField {
    width: 500px;
    height: 500px;
    display: grid;
    grid-template-rows: repeat(10, 1fr);
    grid-template-columns: repeat(10, 1fr);
    border: 1px solid black;
}

.cell {
    width: 50px;
    height: 50px;

}

.snake {
    box-sizing: border-box;
    width: 50px;
    height: 50px;
    background-color: #44AF44;
    border-radius: 10px;
    border: 2px solid #2E7A2F;
}

.head {
    background-color: #44B8AD;
    display: grid;
    grid-template-rows: repeat(10, 1fr);
    grid-template-columns: repeat(5, 1fr);
    position: relative;
}

.head::before {
    content: "";
    color: #2E7A2F;
    width: 8px;
    height: 8px;
    background-color: #2E7A2F;
    grid-column: 2 / span 1;
    grid-row: 2 / span 1;
    border-radius: 2px;
    justify-self: center;
    align-self: center;
}

.head::after {
    content: "";
    color: #2E7A2F;
    width: 8px;
    height: 8px;
    background-color: #2E7A2F;
    grid-column: 4 / span 1;
    grid-row: 2 / span 1;
    border-radius: 2px;
    justify-self: center;
    align-self: center;
}

.apple {
    box-sizing: border-box;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-image: radial-gradient(at top left, #8ffa02, #e80000);
    position: relative;
}

.apple::before {
    content: "";
    width: 5px;
    height: 25px;
    background-color: brown;
    border-radius: 50%/50%;
    transform: rotate(30deg);
    position: absolute;
    top: -15px;
    left: 30px;
}

.apple::after {
    content: "";
    width: 10px;
    height: 20px;
    background-color: rgb(3, 166, 0);
    border-radius: 50%/50%;
    transform: rotate(-30deg);
    position: absolute;
    top: -20px;
    left: 20px;
}
</style>
