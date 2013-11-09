//
//  DOCDetailViewController.h
//  Patient.ly
//
//  Created by Angie Lal on 11/4/13.
//  Copyright (c) 2013 Angie Lal. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "DOCTask.h"

@interface DOCDetailViewController : UIViewController <UISplitViewControllerDelegate>

@property (strong, nonatomic) DOCTask *task;

@property (weak, nonatomic) IBOutlet UILabel *taskIdLabel;
@property (weak, nonatomic) IBOutlet UILabel *nameLabel;
@property (weak, nonatomic) IBOutlet UILabel *descriptionLabel;
@property (weak, nonatomic) IBOutlet UITextView *descriptionTextField;

@end
