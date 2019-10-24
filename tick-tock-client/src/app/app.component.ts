import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { forEach } from '@angular/router/src/utils/collection';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/x-www-form-urlencoded',
    'Access-Control-Allow-Origin': '*'
  })
};
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'tick-tock-client';
  board = [[1, 1, 2], [2, 2, 7], [2, 5, 1]];

  constructor(private http: HttpClient) {}

  move(event) {
    console.log('EVENT', event);
    const row = event.target.parentElement.id;
    const cell = event.target.id;
    console.log('ROW', row);
    console.log('CELL', cell);
    this.board[row][cell] = 1;
    console.log('BOARD', this.board);

    this.http
      .post('http://localhost:5000/nn_move', this.board, httpOptions)
      .subscribe((res: any) => {
        console.log('RES====', res);
        this.board[res[0]][res[1]] = 2;
      });
  }

  isShowX(row, cell) {
    return this.board[row][cell] === 1 ? true : false;
  }

  isShowO(row, cell) {
    return this.board[row][cell] === 2 ? true : false;
  }

  getWinner() {
    let candidate = 0;
    let won = 0;
    // Check rows
    for (let i = 0; i < this.board.length; i++) {
      candidate = 0;
      for (let j = 0; j < this.board[i].length; j++) {
        // Make sure there are no gaps
        if (this.board[i][j] === 0) {
          break;
        }
        // Identify the front-runner
        if (candidate === 0) {
          candidate = this.board[i][j];
        }
        // Determine whether the front-runner has all the slots
        if (candidate !== this.board[i][j]) {
          break;
        } else if (j === this.board[i].length - 1) {
          won = candidate;
        }
        console.log('WON', won);
      }
    }
    console.log('Won', won);
    if (won > 0) {
      return won;
    }
    candidate = 0;
    // Check; columns;
    for (let i = 0; i < this.board[0].length; i++) {
      candidate = 0;
      for (let j = 0; j < this.board.length; j++) {
        if (this.board[j][i] === 0) {
          break;
        }

        if (candidate === 0) {
          candidate = this.board[j][i];
        }
        // Determine whether the front-runner has all the slots
        if (candidate !== this.board[j][i]) {
          break;
        } else if (j === this.board.length - 1) {
          won = candidate;
        }
      }
      if (won > 0) {
        break;
      }
    }
    candidate = 0;
    // Check diagonals
    for (let i = 0; i < this.board.length; i++) {
      if (this.board[i][i] === 0) {
        break;
      }
      console.log('X', candidate);
      if (candidate === 0) {
        candidate = this.board[i][i];
      }
      if (candidate !== this.board[i][i]) {
        break;
      } else if (i === this.board.length - 1) {
        won = candidate;
      }
    }

    console.log('wonD!', won);
    if (won > 0) {
      return won;
    }
    candidate = 0;
    for (let i = 0; i < this.board.length; i++) {
      if (this.board[i][2 - i] === 0) {
        break;
      }
      if (candidate === 0) {
        candidate = this.board[i][2 - i];
      }
      if (candidate !== this.board[i][2 - i]) {
        break;
      } else if (i === this.board.length - 1) {
        won = candidate;
      }

      console.log('wonD2', won);
      if (won > 0) {
        return won;
      }
    }
  }
}
