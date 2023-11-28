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
      'oldPassword': new FormControl('', Validators.required),
      'newPassword': new FormControl('', Validators.required)
    });
  }

  ngOnInit() {}

  async editEmail() {
    if (this.editEmailForm.valid) {
      await this.accountService.updateUser(this.editEmailForm.value.newEmail);
    }
    else{
      console.log("incorrect email was provided: " + this.editEmailForm.value.newEmail);
    }
  }

  async changePassword() {
    if (this.changePasswordForm.valid) {
      await this.accountService.changePassword(this.changePasswordForm.value.oldPassword, this.changePasswordForm.value.newPassword);
    }
    else{
      console.log("incorrect old password: " + this.changePasswordForm.value.oldPassword);
      console.log("incorrect new password: " + this.changePasswordForm.value.newPassword);
    }
  }
}
