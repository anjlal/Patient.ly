//
//  DOCDetailViewController.m
//  Patient.ly
//
//  Created by Angie Lal on 11/4/13.
//  Copyright (c) 2013 Angie Lal. All rights reserved.
//

#import "DOCDetailViewController.h"
#import "DOCMasterViewController.h"
#import "AFNetworking/AFNetworking.h"
#import "DOCTask.h"

@interface DOCDetailViewController ()

@property (strong, nonatomic) UIPopoverController *masterPopoverController;
@property (strong, nonatomic) IBOutlet UIView *containerView;
@property (strong, nonatomic) IBOutlet UIActivityIndicatorView *indicatorView;

- (void)configureView;
@end

@implementation DOCDetailViewController

#pragma mark - Managing the detail item

- (void)setTask:(DOCTask *)newTask
{
    if (_task != newTask) {
        _task = newTask;
        
        // Update the view.
        [self configureView];
    }

    if (self.masterPopoverController != nil) {
        [self.masterPopoverController dismissPopoverAnimated:YES];
    }        
}

- (void)configureView
{
    // Update the user interface for the detail item.

    if (_task) {

        [self.indicatorView stopAnimating];
        _taskIdLabel.text = [NSString stringWithFormat:@"%@", _task.tid];
        _nameLabel.text = _task.name;
        _descriptionTextField.text = _task.issue;
        self.containerView.hidden = NO;

    } else {

        [self.indicatorView startAnimating];
        self.containerView.hidden = YES;

    }
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    [self configureView];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

#pragma mark - Split view

- (void)splitViewController:(UISplitViewController *)splitController willHideViewController:(UIViewController *)viewController withBarButtonItem:(UIBarButtonItem *)barButtonItem forPopoverController:(UIPopoverController *)popoverController
{
    barButtonItem.title = NSLocalizedString(@"Master", @"Master");
    [self.navigationItem setLeftBarButtonItem:barButtonItem animated:YES];
    self.masterPopoverController = popoverController;
}

- (void)splitViewController:(UISplitViewController *)splitController willShowViewController:(UIViewController *)viewController invalidatingBarButtonItem:(UIBarButtonItem *)barButtonItem
{
    // Called when the view is shown again in the split view, invalidating the button and popover controller.
    [self.navigationItem setLeftBarButtonItem:nil animated:YES];
    self.masterPopoverController = nil;
}

@end
