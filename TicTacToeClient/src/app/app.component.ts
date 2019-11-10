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
  board = [0, 0, 0, 0, 0, 0, 0, 0, 0];
  winner = 0;
  winnerTitle = '';
  game = [];
  nn = 2;
  human = 1;
  status = 'Start';
  aiSymvol = '';
  humanSymvol = '';

  constructor(private http: HttpClient) { }

  playAgain() {
    this.status = 'Start';
    this.board = [0, 0, 0, 0, 0, 0, 0, 0, 0];
  }

  pick(player) {
    switch (player) {
      case 'human':
        this.aiSymvol = 'O';
        this.humanSymvol = 'X';
        this.status = 'In Process';
        break;
      case 'ai':
        this.aiSymvol = 'X';
        this.humanSymvol = 'O';
        this.status = 'In Process';
        this.start();
        break;
    }

  }

  start() {
    this.http
      .post('http://0.0.0.0/api/ticky', this.board, httpOptions)
      .pipe(take(1))
      .subscribe((res: any) => {
        this.board[res] = 1;
      });
  }

  move(event) {
    const cell = +event.target.id;
    this.board[cell] = -1;
    if (this.getWinner()) {
      this.http
        .post('http://0.0.0.0/api/ticky', this.board, httpOptions)
        .toPromise()
        .then((res: any) => {
          console.log('res', res);
          console.log('symhu', this.humanSymvol);
          this.board[res] = 1;
          this.getWinner();
        });
    }
  }

  isShowSymvol(cell, symvol) {
    if (((this.board[cell] === 1) && (this.aiSymvol === symvol)) || ((this.board[cell] === -1) && (this.humanSymvol === symvol))) {
      return true;
    } else {
      return false;
    }
  }

  getWinner() {
    // check if all are filled
    let humanWon = false;
    let AIWon = false;
    let isVacent = false;
    for (let i = 0; i < this.board.length; i++) {
      if (this.board[i] == 0) {
        isVacent = true;
      }
    }

    // check for rows
    for (let i = 0; i < this.board.length; i += 3) {
      const rowsum = this.board[i] + this.board[i + 1] + this.board[i + 2];
      if (rowsum === 3) {
        AIWon = true;
      } else if (rowsum === -3) {
        humanWon = true;
      }
    }

    // check cols
    for (let i = 0; i < 3; i++) {
      const colsum = this.board[i] + this.board[i + 3] + this.board[i + 6];
      if (colsum === 3) {
        AIWon = true;
      } else if (colsum === -3) {
        humanWon = true;
      }
    }

    // check digonals
    const sum_ld = this.board[0] + this.board[4] + this.board[8];
    if (sum_ld === 3) {
      AIWon = true;
    } else if (sum_ld === -3) {
      humanWon = true;
    }

    const sum_rd = this.board[2] + this.board[4] + this.board[6];
    if (sum_rd === 3) {
      AIWon = true;
    } else if (sum_rd === -3) {
      humanWon = true;
    }

    if (AIWon) {
      this.status = 'AI';
      return false;
    } else if (humanWon) {
      this.status = 'Human';
      return false;
    } else if (!isVacent) {
      this.status = 'Draw';
      return false;
    } else {
      return true;
    }
  }
}
