//
//  DOCMasterViewController.h
//  Patient.ly
//
//  Created by Angie Lal on 11/4/13.
//  Copyright (c) 2013 Angie Lal. All rights reserved.
//

#import <UIKit/UIKit.h>

@class DOCDetailViewController;

@interface DOCMasterViewController : UITableViewController

@property (strong, nonatomic) DOCDetailViewController *detailViewController;

@end
