import { Component, OnInit } from '@angular/core';
import { AccountService } from '../account.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.css']
})
export class EditProfileComponent implements OnInit{
  editEmailForm: FormGroup;
  changePasswordForm: FormGroup;
  loading = false;

  constructor(
    private fb: FormBuilder, 
    private accountService: AccountService, 
    private router: Router
  ) {
    this.editEmailForm = this.fb.group({
      'newEmail': new FormControl('', [Validators.required, Validators.email])
    });
    this.changePasswordForm = this.fb.group({
      oldPassword: ['', Validators.required],
      newPassword: ['', Validators.required]
    });
  }

  ngOnInit() {}

  async editEmail() {
    console.log(this.editEmailForm);
    console.log(this.editEmailForm.value.newEmail);
    if (this.editEmailForm.valid) {
      await this.accountService.updateUser(this.editEmailForm.value.newEmail);
    }
    else{
      console.log("incorect email");
    }
  }

  async changePassword() {
    if (this.changePasswordForm.valid) {
      await this.accountService.changePassword(this.changePasswordForm.value.oldPassword, this.changePasswordForm.value.newPassword);
    }
  }
}
