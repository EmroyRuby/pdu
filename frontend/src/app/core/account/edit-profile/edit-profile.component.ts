import { Component } from '@angular/core';
import { AccountService } from '../account.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-profile',
  templateUrl: './edit-profile.component.html',
  styleUrls: ['./edit-profile.component.css']
})
export class EditProfileComponent {
  editEmailForm: FormGroup;
  changePasswordForm: FormGroup;

  constructor(private fb: FormBuilder, private accountService: AccountService, private router: Router) {
    this.editEmailForm = this.fb.group({
      newEmail: ['', Validators.required]
    });
    this.changePasswordForm = this.fb.group({
      oldPassword: ['', Validators.required],
      newPassword: ['', Validators.required]
    });
  }

  ngOnInit() {}

  async editEmail() {
    if (this.editEmailForm.valid) {
      await this.accountService.updateUser(this.editEmailForm.value.newEmail);
    }
  }

  async changePassword() {
    if (this.changePasswordForm.valid) {
      await this.accountService.changePassword(this.changePasswordForm.value.oldPassword, this.changePasswordForm.value.newPassword);
    }
  }
}
