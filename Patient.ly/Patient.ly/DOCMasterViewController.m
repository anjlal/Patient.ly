//
//  DOCMasterViewController.m
//  Patient.ly
//
//  Created by Angie Lal on 11/4/13.
//  Copyright (c) 2013 Angie Lal. All rights reserved.
//

#import "DOCMasterViewController.h"

#import "DOCDetailViewController.h"
#import <AFNetworking/AFNetworking.h>

@interface DOCMasterViewController ()

@property (strong, nonatomic) NSMutableArray *objects;

@end

@implementation DOCMasterViewController

- (void)awakeFromNib
{
    self.clearsSelectionOnViewWillAppear = NO;
    self.preferredContentSize = CGSizeMake(320.0, 600.0);
    [super awakeFromNib];

}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    self.navigationItem.leftBarButtonItem = self.editButtonItem;

    UIBarButtonItem *addButton = [[UIBarButtonItem alloc] initWithBarButtonSystemItem:UIBarButtonSystemItemAdd target:self action:@selector(insertNewObject:)];
    self.navigationItem.rightBarButtonItem = addButton;
    self.detailViewController = (DOCDetailViewController *)[[self.splitViewController.viewControllers lastObject] topViewController];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)insertNewObject:(id)sender
{
    if (!self.objects) {
        self.objects = [NSMutableArray array];
    }
    AFHTTPRequestOperationManager *manager = [AFHTTPRequestOperationManager manager];

    [manager GET:@"http://localhost:5000/"
      parameters:nil
         success:^(AFHTTPRequestOperation *operation, id responseObject) {
             NSLog(@"Type: %@", [responseObject[@"patients"] class]);

             NSLog(@"JSON: %@", responseObject);
             [_objects addObjectsFromArray:responseObject[@"patients"]];
             [self.tableView reloadData];

             //[_objects insertObject:responseObject[@"patients"] atIndex:0];

             //NSIndexPath *indexPath = [NSIndexPath indexPathForRow:0 inSection:0];
             //[self.tableView insertRowsAtIndexPaths:@[indexPath] withRowAnimation:UITableViewRowAnimationAutomatic];

         } failure:^(AFHTTPRequestOperation *operation, NSError *error) {
             NSLog(@"This request failed: %@", error);
         }];


//    NSString *patient = @"{ \"Patient\": {\"Name\": \"Angie\"} }";
    //NSString *patient = responseObject;
    //NSData *patientData = [patient dataUsingEncoding:NSUTF8StringEncoding];

    //             NSError *error;
    //             id patientObject = [NSJSONSerialization JSONObjectWithData:patientData options:0 error: &error];
    //             NSDictionary *patientDictionary = patientObject;
    //             if (error){
    //                 NSLog(@"Error: %@", error);
    //             }
    //NSLog(@"%@", patientDictionary);
    //[_objects insertObject:responseObject[@"patients"][@"name"] atIndex:0];

}

#pragma mark - UITableViewDataSource

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView
{
    return 1;
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return _objects.count;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:@"Cell" forIndexPath:indexPath];

    NSDictionary *object = self.objects[indexPath.row];
    cell.textLabel.text = object[@"name"];
    return cell;
}

#pragma mark - UITableViewDelegate

- (BOOL)tableView:(UITableView *)tableView canEditRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the specified item to be editable.
    return YES;
}

- (void)tableView:(UITableView *)tableView commitEditingStyle:(UITableViewCellEditingStyle)editingStyle forRowAtIndexPath:(NSIndexPath *)indexPath
{
    if (editingStyle == UITableViewCellEditingStyleDelete) {
        [self.objects removeObjectAtIndex:indexPath.row];
        [tableView deleteRowsAtIndexPaths:@[indexPath] withRowAnimation:UITableViewRowAnimationFade];
    } else if (editingStyle == UITableViewCellEditingStyleInsert) {
        // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view.
    }
}

/*
// Override to support rearranging the table view.
- (void)tableView:(UITableView *)tableView moveRowAtIndexPath:(NSIndexPath *)fromIndexPath toIndexPath:(NSIndexPath *)toIndexPath
{
}
*/

/*
// Override to support conditional rearranging of the table view.
- (BOOL)tableView:(UITableView *)tableView canMoveRowAtIndexPath:(NSIndexPath *)indexPath
{
    // Return NO if you do not want the item to be re-orderable.
    return YES;
}
*/

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath
{
    NSDate *object = self.objects[indexPath.row];
    self.detailViewController.detailItem = object;
}

@end
