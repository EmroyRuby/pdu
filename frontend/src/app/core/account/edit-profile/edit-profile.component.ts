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
  modalText: string = '';

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
    try{
      await this.accountService.updateUser(this.editEmailForm.value.newEmail);
    }
    catch(e: any){
      console.log(e.error);
      this.modalText = e.error.email[0];
      document.getElementById("openModal")?.click();
    }
  }

  async changePassword() {
    try{
      await this.accountService.changePassword(this.changePasswordForm.value.oldPassword, this.changePasswordForm.value.newPassword);
    }
    catch(e: any){
      console.log(e.error);
      this.modalText = '';
      if (e.error.new_password !== undefined){
        this.modalText += "New password error:\n";
        e.error.new_password.forEach((element: any) => {
          this.modalText += String(element) + '\n';
        });
      }
      else if (e.error.old_password !== undefined){
        this.modalText += "Current password error:\n";
        e.error.old_password.forEach((element: any) => {
          this.modalText += String(element) + '\n';
        });
      }
      document.getElementById("openModal")?.click();
    }
  }
}
