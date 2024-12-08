import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HelpComponent } from './help.component';

describe('HelpComponent', () => {
  let component: HelpComponent;
  let fixture: ComponentFixture<HelpComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HelpComponent]
    });
    fixture = TestBed.createComponent(HelpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should display the correct number of help links', () => {
    const helpLinks = fixture.nativeElement.querySelectorAll('.help-link');
    expect(helpLinks.length).toBe(component.helpLinks.length);
  });
});
