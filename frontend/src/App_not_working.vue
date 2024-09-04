<template>
  <div id="main-container" class="mainContainer">
    <div id="game" class="playingField">  
      <div
        v-for="segment of snakeCoordinates" 
        class="snake"
        :style="segment.positionStyle"
        :key="segment.id"
      ></div>
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

<script>
export default {
  data() {
    return {
      snakeCoordinates: [],
      fieldWidth: null,
      fieldHeight: null,
    };
  },
  methods: { // создаешь методы, которые можно вызывать, чтобы менять состояние в произвольный момент времени
    handleFormSubmit() {
        resizeField();
        restartGame();
        const pauseButton = document.getElementById('pauseButton');
        if (pauseButton.innerText === 'Resume') {
            clearInterval(gameCycle);
        };
    },

    resizeField() {
        const field = document.getElementById('game');
        field.style.cssText += `
            width: ${cellSizePx * fieldWidth}px;
            height: ${cellSizePx * fieldHeight}px;
            grid-template-rows: repeat(${fieldHeight}, 1fr);
            grid-template-columns: repeat(${fieldWidth}, 1fr);
        `;
    },
    
    elongateSnek() {
      let newSegment = document.createElement('div');
      document.getElementById('game').appendChild(newSegment);
      newSegment.style.visibility = 'hidden';
      newSegment.className = 'snake';
      newSegment.id = `${++segment_id}`;

      this.snakeCoordinates.push({
          x,
          y,
          direction,
          element: document.getElementById(newSegment.id),
          positionStyle: `
            grid-column: ${x + 1} / span 1;
            grid-row: ${y + 1} / span 1;`
      });
    },

    spawnApple() {
      let x, y;
      while (true) {
          x = Math.floor(Math.random() * fieldWidth);
          y = Math.floor(Math.random() * fieldHeight);
          if (!snakeCoordinates.find(item => item.x === x && item.y === y)) {
              break;
          }
      }
      apple.x = x;
      apple.y = y;
    },
    
    moveSnek() {
      let head = snakeCoordinates[0];
      newDirection = turnDirections.shift();

      if (newDirection != undefined && newDirection != opposites[head.direction] && newDirection != direction) {
          direction = newDirection;
          turns.push({x: head.x, y: head.y, direction: direction});
      }

      if (turns.length > 0) {
          for (let i = turns.length - 1; i >= 0; i--) {
              let turn = turns[i];
              let snakeBend = snakeCoordinates.find(item => item.x === turn.x && item.y === turn.y);
              if (snakeBend === undefined) {
                  turns.shift();
              } else {
                  snakeBend.direction = turn.direction;
              }
          }
      }

      let {x, y, direction: tail_direction} = snakeCoordinates.at(-1);

      for (segment of snakeCoordinates) {
          if (segment.direction === 'left') {
              segment.x--;
          } else if (segment.direction === 'right') {
              segment.x++;
          } else if (segment.direction === 'up') {
              segment.y--;
          } else if (segment.direction === 'down') {
              segment.y++;
          }
      }
      
      if (head.x >= fieldWidth || head.y >= fieldHeight || head.x < 0 || head.y < 0 ||
          snakeCoordinates.filter(item => item.x === head.x && item.y === head.y).length > 1
      ) {
          gameOver();
      }

      if (head.x === apple.x && head.y === apple.y) {
          elongateSnek(x, y, tail_direction);
          respawnApple();
      }
    },

    gameOver() {
        clearInterval(gameCycle);
        let restart = confirm("Game Over. Try again?");
        if (restart) {
            restartGame();
        }
    },

    restartGame() {
      for (segment of snakeCoordinates) {
          segment.element.remove()
      }
      snakeCoordinates.length = 0;
      segment_id = 1;
      spawn();
      gameCycle = setInterval(() => {
          moveSnek();
          drawState();
      }, 250);
    },

    pause() {
        const pauseButton = document.getElementById('pauseButton');
        const pauseUnpause = function() {
            if (pauseButton.innerText === 'Pause') {
                clearInterval(gameCycle);
                pauseButton.innerText = 'Resume';
            }
            else {
                gameCycle = setInterval(() => {
                    moveSnek();
                    drawState();
                }, 250);
                pauseButton.innerText = 'Pause';
            }
        }
        pauseButton.addEventListener('click', pauseUnpause);
    },
  },
  created() { // выполняешь действия, которые необходимо выполнить один раз в начале всей игры
    let fieldWidth = 10;
    let fieldHeight = 10;
    const cellSizePx = 50;
    const turns = [];
    const turnDirections = [];

    const opposites = {
        'left': 'right',
        'right': 'left',
        'up': 'down',
        'down': 'up',
    };

    const rotationDegrees = {
        'left': 270,
        'right': 90,
        'up': 0,
        'down': 180,
    };

    let direction,
        newDirection;
    
    const apple = {
        x: null,
        y: null,
        element: null,
    }

    let segment_id = 1;

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

    this.spawn();
    this.initializeApple();
    this.pause();
    let gameCycle = setInterval(() => {
        this.moveSnek();
    }, 250);

    const dimensionsForm = document.getElementById('dimensions-form');
    dimensionsForm.elements.width.value = `${fieldWidth}`;
    dimensionsForm.elements.height.value = `${fieldHeight}`;
    dimensionsForm.addEventListener('submit', handleFormSubmit);
  },
}

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
