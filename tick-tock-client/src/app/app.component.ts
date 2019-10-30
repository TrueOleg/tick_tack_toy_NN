import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { take } from 'rxjs/operators';

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
  board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  winner = 0;
  winnerTitle = '';
  game = [];

  constructor(private http: HttpClient) {}

  logGame(player, row, cell) {
    const step = [player, [row, cell]];
    this.game.push(step);
    console.log('GAME', this.game);
  }

  start() {
    this.http
      .post('http://localhost:5000/nn_move', this.board, httpOptions)
      .pipe(take(1))
      .subscribe((res: any) => {
        console.log('RES====', res);
        this.board[res[0]][res[1]] = 1;
        const step = [1, res];
        this.game.push(step);
        console.log('GAME', this.game);
      });
  }

  move(event) {
    const row = +event.target.parentElement.id;
    const cell = +event.target.id;
    this.board[row][cell] = 1;
    console.log('row', row);
    console.log('cell', cell);
    console.log('board', this.board);
    this.logGame(1, row, cell);
    if (this.getWinner() === 0 && this.board.length !== 9) {
      this.http
        .post('http://localhost:5000/nn_move', this.board, httpOptions)
        .toPromise()
        .then((res: any) => {
          this.board[res[0]][res[1]] = 2;
          console.log('row', res[0]);
          console.log('cell', res[1]);
          console.log('board', this.board);
          this.logGame(2, res[0], res[1]);
          if (this.getWinner() === 2) {
            this.winner = this.getWinner();
            this.winnerTitle = 'Comp';
            this.http
              .post('http://localhost:5000/history', this.game, httpOptions)
              .subscribe(res => console.log('res', res));
          } else if (this.getWinner() === 3) {
            this.winner = this.getWinner();
            this.winnerTitle = 'NONE';
            this.http
              .post('http://localhost:5000/history', this.game, httpOptions)
              .subscribe(res => console.log('res', res));
          }
        });
    } else {
      this.winner = this.getWinner();
      this.winnerTitle = this.winner === 1 ? 'Human' : 'None';
      this.http
        .post('http://localhost:5000/history', this.game, httpOptions)
        .subscribe(res => console.log('res', res));
    }
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
      }
    }
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
      if (candidate === 0) {
        candidate = this.board[i][i];
      }
      if (candidate !== this.board[i][i]) {
        break;
      } else if (i === this.board.length - 1) {
        won = candidate;
      }
    }

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

      if (won > 0) {
        return won;
      }
    }
    const haveNull = this.board.some(el => {
      return el.includes(0);
    });
    if (!haveNull) {
      won = 3;
    }
    return won;
  }
}
