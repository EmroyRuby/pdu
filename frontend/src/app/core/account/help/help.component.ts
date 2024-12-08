import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-help',
  templateUrl: './help.component.html',
  styleUrls: ['./help.component.css']
})
export class HelpComponent implements OnInit {
  // Define the helpLinks array with video links
  helpLinks = [
    {
      'title': 'How to Sign Up for the Event',
      'url': 'https://drive.google.com/file/d/1hnTxgZFVm0ENaEkbrpm9drkSOiDsANWn/view?usp=drive_link'
    },
    {
      'title': 'How to Create an Event',
      'url': 'https://drive.google.com/file/d/1BPtKncdlaLO0KounhN8qFPtiWAIZgBch/view?usp=drive_link'
    },
    {
      'title': 'How to Edit an Event',
      'url': 'https://drive.google.com/file/d/1DYKpqumltbqZayYK7_pkUKrr160eqqjy/view?usp=drive_link'
    },
    {
      'title': 'How to Edit Your Profile Data',
      'url': 'https://drive.google.com/file/d/11AANkFHq3qpAD_qWT5itgPJ-tWaUfaY_/view?usp=drive_link'
    },
    {
      'title': 'How to Add a Comment',
      'url': 'https://drive.google.com/file/d/1yNyofk1a4tIiB_u6F2Ov22ADjhuIXquL/view?usp=drive_link'
    }
  ];

  constructor() {}

  ngOnInit(): void {}
}
